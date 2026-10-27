#!/usr/bin/env python3
"""Exact nine-XOR cyclic parity minimum. Produced by Nick Petalas; Apache-2.0."""
from hashlib import sha256
import json
from pathlib import Path

WIDTH = 5
MASK = 31
GATES = tuple((src, dst) for src in range(WIDTH)
              for dst in range(WIDTH) if src != dst)
WORD = ((0, 2), (0, 4), (3, 0), (4, 3), (1, 4),
        (0, 1), (2, 1), (1, 0), (3, 2))
FILES = ("PROOF.md", "README.md", "SOURCES.json", "TASK.json", "VERIFY.json", "verify.py")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(rows):
    require(len(rows) == WIDTH, "exactly five rows required")
    require(all(type(r) is int and 0 <= r <= MASK for r in rows), "invalid row")
    return sum(row << (WIDTH * i) for i, row in enumerate(rows))


def step(state, gate):
    src, dst = gate
    require(type(state) is int and 0 <= state < 1 << 25, "invalid matrix")
    require(gate in GATES, "invalid directed XOR")
    return state ^ (((state >> (WIDTH * src)) & MASK) << (WIDTH * dst))


def ball(center):
    """Enumerate all words of length at most four, merging equal matrices."""
    seen = {center}
    frontier = {center}
    counts = [1]
    for _ in range(4):
        following = set()
        for state in frontier:
            for gate in GATES:
                nxt = step(state, gate)
                if nxt not in seen:
                    following.add(nxt)
        require(not seen.intersection(following), "distance layers overlap")
        seen.update(following)
        frontier = following
        counts.append(len(frontier))
    return seen, counts


def literal_word(value, word):
    require(type(value) is int and 0 <= value <= MASK, "invalid input")
    require(len(word) <= 9 and all(g in GATES for g in word), "invalid word")
    registers = [(value >> i) & 1 for i in range(WIDTH)]
    for src, dst in word:
        registers[dst] ^= registers[src]
    return sum(bit << i for i, bit in enumerate(registers))


def literal_target(value):
    return sum((((value >> i) ^ (value >> ((i + 1) % WIDTH))
                 ^ (value >> ((i + 2) % WIDTH))) & 1) << i
               for i in range(WIDTH))


def check_word_and_controls(identity, target):
    state = identity
    for gate in WORD:
        old = state
        state = step(state, gate)
        require(step(state, gate) == old, "gate is not involutive")
    require(state == target, "word has the wrong complete endpoint")
    outputs = [literal_word(value, WORD) for value in range(32)]
    require(outputs == [literal_target(value) for value in range(32)], "truth table")
    require(len(set(outputs)) == 32, "endpoint loses arbitrary input information")
    require(all(literal_word(outputs[v], WORD[::-1]) == v for v in range(32)), "inverse")
    for omitted in range(9):
        shorter = WORD[:omitted] + WORD[omitted + 1:]
        require(any(literal_word(v, shorter) != literal_target(v)
                    for v in range(32)), "omitted gate was undetected")
    for value, word in ((-1, WORD), (32, WORD), (True, WORD), (0, ((0, 0),)),
                        (0, ((5, 0),)), (0, WORD + WORD)):
        try:
            literal_word(value, word)
        except ValueError:
            continue
        raise ValueError("invalid literal program accepted")
    for rows in ((1, 2), (1, 2, 4, 8, 32), (True, 2, 4, 8, 16)):
        try:
            encode(rows)
        except ValueError:
            continue
        raise ValueError("invalid matrix accepted")
    return {"truth_table_inputs": 32, "deleted_gate_controls": 9,
            "invalid_input_controls": 9}


def main():
    identity = encode([1 << i for i in range(WIDTH)])
    rows = [(1 << i) | (1 << ((i + 1) % WIDTH))
            | (1 << ((i + 2) % WIDTH)) for i in range(WIDTH)]
    target = encode(rows)
    controls = check_word_and_controls(identity, target)
    forward, fcounts = ball(identity)
    backward, bcounts = ball(target)
    require(fcounts == [1, 20, 260, 2570, 19680], "identity radius counts")
    require(bcounts == fcounts, "target radius counts")
    intersection = forward.intersection(backward)
    require(not intersection, "a word of at most eight XORs exists")
    # A known eight-gate endpoint must be detected by the same exclusion method.
    midpoint = identity
    for gate in WORD[:4]:
        midpoint = step(midpoint, gate)
    require(midpoint in forward, "known four-gate midpoint missing")
    short_endpoint = literal_matrix(WORD[:8], identity)
    nearby, nearcounts = ball(short_endpoint)
    require(midpoint in nearby and nearcounts == fcounts, "false-negative control")
    require(not (forward & backward), "negative certificate changed")
    root = Path(__file__).resolve().parent
    hashes = {}
    for name in FILES:
        path = root / name
        require(path.is_file() and path.stat().st_size <= 1 << 20, "source size")
        hashes[name] = sha256(path.read_bytes()).hexdigest()
    receipt = {"status": "PASS_FIVE_ROLE_CYCLIC_PARITY", "claim_type": "finite certificate",
               "minimum_xors": 9, "target_rows": rows, "word": WORD,
               "forward_layers": fcounts, "backward_layers": bcounts,
               "ball_size": len(forward), "intersection_size": len(intersection),
               "eight_gate_positive_controls": 1, **controls, "sha256": hashes}
    print(json.dumps(receipt, sort_keys=True, indent=2))


def literal_matrix(word, identity):
    state = identity
    for gate in word:
        state = step(state, gate)
    return state


if __name__ == "__main__":
    main()
