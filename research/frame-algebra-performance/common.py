"""Pinned input checks shared by the benchmark, adapter and tests."""
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
SOURCE = json.loads((ROOT/'SOURCE.json').read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_source(directory):
    directory = Path(directory).resolve()
    paths = list(directory.rglob('*'))
    if any(p.is_symlink() for p in paths):
        raise ValueError('source package must not contain symlinks')
    actual = {p.relative_to(directory).as_posix() for p in paths if p.is_file()}
    if actual != set(SOURCE['files']):
        raise ValueError('source file set differs from the pinned package')
    for name, digest in SOURCE['files'].items():
        if sha(directory/name) != digest:
            raise ValueError('source hash mismatch: '+name)
    return directory


def reference_functions():
    """Compile the two unchanged AST nodes; no numpy dependency for unit tests."""
    path = ROOT/'reference/stagelib.py'
    if sha(path) != SOURCE['files']['code/stagelib.py']:
        raise ValueError('reference stagelib.py differs from the immutable source')
    parsed = ast.parse(path.read_text())
    nodes = [node for node in parsed.body if isinstance(node, ast.FunctionDef)
             and node.name in ('rank_q', 'key_of')]
    if len(nodes) != 2:
        raise ValueError('missing reference functions')
    namespace = {'Fraction': Fraction}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    return SimpleNamespace(rank_q=namespace['rank_q'], key_of=namespace['key_of'])


def verify_outputs(directory):
    directory = Path(directory)
    result = {}
    for stage, pins in SOURCE['outputs'].items():
        result[stage] = {}
        for name, digest in pins.items():
            got = sha(directory/stage/name)
            if got != digest:
                raise ValueError('output hash mismatch: '+stage+'/'+name)
            result[stage][name] = got
    pricing = json.loads((directory/'F/kappa.json').read_text())
    if pricing['kappa'] != SOURCE['expected_kappa']:
        raise ValueError('final exact kappa changed')
    if Path(pricing.pop('word')).resolve() != (directory/'F').resolve():
        raise ValueError('pricing receipt is bound to another output')
    return result, pricing
