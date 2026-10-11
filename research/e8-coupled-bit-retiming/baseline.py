"""Run every check of pinned PR375 with explicit shell/interpreter transport."""
from pathlib import Path
import argparse,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
def run(output,shell='bash',boost=None):
    source=ROOT/'vendor/source375';output=Path(output).resolve()
    output.mkdir(parents=True,exist_ok=False)
    script=(source/'verify.sh').read_text(encoding='utf-8')
    declaration='HERE=$(cd "$(dirname "$0")" && pwd); WD=$(mkdir -p "$1" && cd "$1" && pwd)'
    assert script.count(declaration)==1 and script.count('PY="python3 -B"')==1
    script=script.replace(declaration,'HERE=$SOURCE375; WD=$VERIFY_OUT')
    script=script.replace('set -euo pipefail',"set -euo pipefail\nIFS=$'\\n\\t'")
    if sys.platform=='win32':
        definitions='\n'.join(f'{name}() {{ "$VERIFY_PYTHON" -B "$TRANSPORT_UTILS" {name} "$@"; }}' for name in ('sha256sum','tee','tail','cmp','gunzip','mkdir','cp'))
        script=script.replace('IFS=$\'\\n\\t\'',"IFS=$'\\n\\t'\n"+definitions)
        script='\n'.join(('native '+line if line.startswith('$BIN/') else line) for line in script.splitlines())+'\n'
        script=script.replace(definitions,definitions+'\nnative() { "$VERIFY_PYTHON" -B "$NATIVE_TRANSPORT" "$@"; }')
    script=script.replace('PY="python3 -B"','PY=py; py() { "$VERIFY_PYTHON" -B "$RUN_PINNED" "$@"; }')
    transport=output/'transport.sh';transport.write_text(script,encoding='utf-8',newline='\n')
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',SOURCE375=source.as_posix(),VERIFY_OUT=output.as_posix(),VERIFY_PYTHON=Path(sys.executable).as_posix(),RUN_PINNED=(ROOT/'run_pinned.py').as_posix(),TRANSPORT_UTILS=(ROOT/'transport_utils.py').as_posix())
    env['NATIVE_TRANSPORT']=(ROOT/'native_transport.py').as_posix()
    if boost:env['CPLUS_INCLUDE_PATH']=str(Path(boost).resolve())
    with (output/'VERIFY-LOG.txt').open('w',encoding='utf-8',newline='\n') as stream:
        subprocess.run([shell,str(transport),str(output)],cwd=output,env=env,stdout=stream,stderr=subprocess.STDOUT,check=True)
    return output
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output');ap.add_argument('--shell',default='bash');ap.add_argument('--boost-include');a=ap.parse_args()
    run(a.output,a.shell,a.boost_include);print('PASS full pinned PR375 baseline')
