#!/bin/sh
# Reproduce every number in README.md from the pinned repository files (standard library; order_model.py needs ortools).
# usage: research/complex-delivery-rigidity/reproduce.sh WORKDIR   (run from the repository root)
set -eu
W=${1:?usage: reproduce.sh WORKDIR}; H=research/complex-delivery-rigidity; C=$H/code; R=$W/results; mkdir -p "$R"
IN=research/direct-delivery504-global/inputs/hamming; K=research/complex-571-cold14-k492
python3 -B "$C/instrument_constructor.py" --constructor "$K/code/construct_k_triangle.py" --inputs "$IN" --tri empty --out "$W/raw504"
python3 -B "$C/instrument_constructor.py" --constructor "$K/code/construct_k_triangle.py" --inputs "$IN" --tri "$K/data/TRI-SCHEDULE.json" --out "$W/raw492"
python3 -B "$C/blockdata.py" "$W/raw504/ROLES.json" "$IN/PROTOTYPE.json" "$R/blocks.json" | tee "$R/blockdata.log"
python3 -B "$C/own_deferral.py" "$W/raw504/FULL-WORD.json.gz" "$W/raw504/ROLES.json" "$R/own_deferral.json"
python3 -B "$C/read_audit.py" "$W/raw504/FULL-WORD.json.gz" "$W/raw504/ROLES.json" "$R/blocks.json" "$R/read_audit.json"
python3 -B "$C/tolerance.py" "$IN/PROTOTYPE.json" "$W/raw504/ROLES.json" "$R/tolerance.json" | tee "$R/tolerance.log"
python3 -B "$C/census.py" "$W/raw504/FULL-WORD.json.gz" "$R/census504.json" | tee "$R/census504.log"
if python3 -c "import ortools" 2>/dev/null; then
  python3 -B "$C/order_model.py" "$R/blocks.json" 1 60 A 1 first | tee "$R/order_A1.log"
  python3 -B "$C/order_model.py" "$R/blocks.json" 2 60 B 1 first | tee "$R/order_B2.log"
  python3 -B "$C/order_model.py" "$R/blocks.json" 3 240 A 1 first | tee "$R/order_A3.log"
else echo "ortools not installed: order_model.py skipped (results/order_*.log hold the recorded runs)"; fi
echo DONE
