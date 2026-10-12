#!/usr/bin/env bash
set -euo pipefail
package_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
python_bin="${CYCLIC_SCAN_PYTHON:-python3}"
"${python_bin}" -I -O -B "${package_dir}/verify.py" --work "${1:?provide an empty output directory}"
