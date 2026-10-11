"""Small byte-preserving transports for Windows shells without coreutils."""
from pathlib import Path
import gzip,hashlib,shutil,sys
command,args=sys.argv[1],sys.argv[2:]
if command=='sha256sum':
    assert '-c' in args
    manifest=Path(args[args.index('-c')+1])
    for line in manifest.read_text(encoding='utf-8').splitlines():
        digest,name=line.split(None,1);name=name.lstrip('*')
        actual=hashlib.sha256(Path(name).read_bytes()).hexdigest()
        if actual!=digest:raise SystemExit('SHA256 mismatch: '+name)
elif command=='tee':
    data=sys.stdin.buffer.read();Path(args[0]).write_bytes(data);sys.stdout.buffer.write(data)
elif command=='tail':
    assert args==['-1']
    lines=sys.stdin.buffer.read().splitlines(keepends=True)
    if lines:sys.stdout.buffer.write(lines[-1])
elif command=='cmp':
    assert len(args)==2
    if Path(args[0]).read_bytes()!=Path(args[1]).read_bytes():raise SystemExit('Byte comparison differs')
elif command=='gunzip':
    assert args[0]=='-c'
    for name in args[1:]:sys.stdout.buffer.write(gzip.decompress(Path(name).read_bytes()))
elif command=='mkdir':
    assert args[0]=='-p'
    for name in args[1:]:Path(name).mkdir(parents=True,exist_ok=True)
elif command=='cp':
    assert len(args)==3 and args[0]=='-r'
    source,target=map(Path,args[1:])
    if target.is_dir():target=target/source.name
    shutil.copytree(source,target)
else:raise SystemExit('Unknown transport command')
