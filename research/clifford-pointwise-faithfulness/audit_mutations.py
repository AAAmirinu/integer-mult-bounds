"""Check that the scientific replay rejects four deliberate defects.

Each check uses a private copy. No source input is changed.
Ali Romman, with substantial OpenAI Codex assistance. Apache-2.0.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CASES = (
    ("first Clifford overlap", "bounds.py", "counts[1] //= 2", "counts[1] //= 1",
     "Exact first Clifford overlap level"),
    ("native phase outside tensor", "native_pointwise.py",
     "coefficient*exact.power(phase, width)", "coefficient*phase", "Native/scalar phase residue"),
    ("projection scale outside tensor", "stabilizer.py", "value*power(ratio, width)",
     "value*ratio", "Stabilizer pointwise Gram estimate"),
    ("unsigned fixed Pauli count", "census.py", "trace += 1 if delta == 0 else -1",
     "trace += 1", "Nonzero-trace Pauli fiber count"),
)


def run():
    rows = []
    with tempfile.TemporaryDirectory(prefix="clifford-pointwise-mutations-") as directory:
        root = Path(directory)
        package = root / "research" / HERE.name
        shutil.copytree(HERE, package)
        for item in json.loads((HERE / "SOURCES.json").read_text())["files"]:
            if item["usage"] == "input":
                target = root / item["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / item["path"], target)
        for label, name, old, new, diagnostic in CASES:
            target = package / name
            original = target.read_text()
            if original.count(old) != 1:
                raise ValueError("Mutation target is not unique: "+label)
            target.write_text(original.replace(old, new))
            for optimized in (False, True):
                argv = [sys.executable, "-I"]+(["-O"] if optimized else [])
                argv += ["-W", "error", "-B", str(package / "verify.py")]
                result = subprocess.run(argv, capture_output=True, text=True, timeout=180)
                if result.returncode == 0 or diagnostic not in result.stderr:
                    raise ValueError("Mutation did not fail as expected: "+label+"\n"+result.stderr)
                rows.append({"mutation": label, "optimized": optimized, "diagnostic": diagnostic})
            target.write_text(original)
    sources = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
               for path in sorted(HERE.glob("*.py"))}
    return {"status": "PASS_EIGHT_POINTWISE_MUTATION_REJECTIONS", "checks": rows,
            "source_sha256": sources}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    result = run()
    path = HERE / "MUTATIONS.json"
    if args.write_result:
        path.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    elif result != json.loads(path.read_text()):
        raise ValueError("The mutation receipt changed")
    print(result["status"])


if __name__ == "__main__":
    main()
