#!/usr/bin/env python3
"""Exercise fail-closed package/source pins under normal and optimized Python."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    cases = (
        ("changed_reference_with_updated_manifest", "reference git blob mismatch"),
        ("changed_fixture", "package hash mismatch: fixtures.json"),
        ("missing_fixture", "package file inventory mismatch"),
        ("unexpected_file", "package file inventory mismatch"),
    )
    receipts = []
    with tempfile.TemporaryDirectory(prefix="exact log controls ") as temp:
        root = Path(temp)
        for name, reason in cases:
            package = root / name
            shutil.copytree(HERE, package, ignore=shutil.ignore_patterns("__pycache__"))
            if name == "changed_reference_with_updated_manifest":
                path = package / "reference/base_two_moment.py"
                path.write_bytes(path.read_bytes() + b"# changed\n")
                mf = package / "MANIFEST.json"
                data = json.loads(mf.read_text())
                data["reference/base_two_moment.py"] = hashlib.sha256(path.read_bytes()).hexdigest()
                mf.write_text(json.dumps(data, indent=2) + "\n")
            elif name == "changed_fixture":
                path = package / "fixtures.json"
                path.write_bytes(path.read_bytes() + b" \n")
            elif name == "missing_fixture":
                (package / "fixtures.json").unlink()
            else:
                (package / "unlisted.json").write_text("{}\n")
            for optimized in (False, True):
                command = [sys.executable, "-I", "-B"] + (["-O"] if optimized else [])
                command += [str(package / "verify.py")]
                result = subprocess.run(command, capture_output=True, text=True, timeout=20)
                require(result.returncode == 1, "wrong exit status: " + name)
                require(result.stderr.strip() == "FAIL: " + reason, "wrong failure reason: " + name)
                require("PASS_EXACT_LOG_HORNER" not in result.stdout, "false success marker")
                receipts.append({"case": name, "optimization_level": int(optimized), "rejection": reason})
    print(json.dumps({"status": "PASS_PACKAGE_CONTROLS", "rejected": len(receipts), "cases": receipts}, indent=2))


if __name__ == "__main__":
    main()
