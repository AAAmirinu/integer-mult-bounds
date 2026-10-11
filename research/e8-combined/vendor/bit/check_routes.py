"""Verify the frozen bit owner routes with independent exact arithmetic."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
import argparse
import gzip
import hashlib
import json


parser = argparse.ArgumentParser()
parser.add_argument("--base", type=Path, required=True)
parser.add_argument("--word", type=Path, required=True)
args = parser.parse_args()
BASE, WORD = args.base, args.word
PATHS = [BASE / "GLOBAL-TEMPLATE.json.gz", BASE / "GEOMETRY.json",
         BASE / "local/records/249-states.json", BASE / "local/records/frames.json",
         BASE / "local/isometries.json", WORD]
inputs = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in PATHS}


def read(path):
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == ".gz" else data)


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    columns = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in columns] for row in a]


def rank(a):
    rows = [[Q(x) for x in row] for row in a]
    r = 0
    for j in range(8):
        p = next((i for i in range(r, len(rows)) if rows[i][j]), None)
        if p is None:
            continue
        rows[p], rows[r] = rows[r], rows[p]
        scale = rows[r][j]
        rows[r] = [x / scale for x in rows[r]]
        for i in range(r + 1, len(rows)):
            scale = rows[i][j]
            rows[i] = [x - scale * y for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def elementary_cost(a):
    a = [row[:] for row in a]
    count, coefficients, scales = 0, [], []
    for j in range(len(a)):
        p = next(i for i in range(j, len(a)) if a[i][j])
        if p != j:
            a[p], a[j] = a[j], a[p]
            count += 1
        if a[j][j] != 1:
            c = 1 / a[j][j]
            coefficients.append(c)
            scales.append(c)
            a[j] = [c * x for x in a[j]]
            count += 1
        for i in range(len(a)):
            if i != j and a[i][j]:
                c = -a[i][j]
                coefficients.append(c)
                a[i] = [x + c * y for x, y in zip(a[i], a[j])]
                count += 1
    assert a == identity(len(a))
    return count, coefficients, scales


def swap_cost(p):
    unseen = set(range(len(p)))
    cycles = 0
    while unseen:
        i = min(unseen)
        while i in unseen:
            unseen.remove(i)
            i = p[i]
        cycles += 1
    return len(p) - cycles


t, geo, state, frame_file, iso, word = map(read, PATHS)
frames = frame_file["frames"]
M, H, V, R = geo["m"], word["h"], word["v"], word["R"]
LOCAL = 2 * V + R
EXPECTED_HELPERS = t["stages"] * t["replicas"] * R
assert (M, H, V) == (78, 8, 120)
assert (t["m"], t["h"], t["stages"], t["replicas"], t["live"]) == (M, H, 11, 4, 4800)
assert (state["R"], state["n"], word["R"], word["v"]) == (R, LOCAL, R, V)
assert all(frames[str(state["final"][str(j)])]["dim"] == H for j in range(2 * V, LOCAL))
assert t["residual_isometries"] == iso
assert t["geometry_sha256"] == inputs[str(BASE / "GEOMETRY.json")]
assert geo["m"] == M and geo["h"] == H and geo["stages"] == 11
assert len(geo["ports"]) == V

# Derive each coordinate residual from its exported physical entrance frame.
residuals = {}
for record in iso:
    f, e = record["frame"], record["entrance_rank"]
    assert f not in residuals and e == frames[str(f)]["dim"]
    entrance = frames[str(f)]["B"]
    support = {j for row in entrance for j, x in enumerate(row) if x}
    assert len(support) == rank(entrance) == e
    axes = set(range(H)) - support
    matrix = [[Q(x, record["denominator"]) for x in row] for row in record["orthogonal_rows_numerator"]]
    assert len(matrix) == H and multiply(matrix, transpose(matrix)) == identity(H)
    assert all(row.count(1) == 1 and row.count(0) == H - 1 for row in matrix)
    ids = record["entrance_basis"] + record["residual_basis"]
    assert [word["lines"][j] for j in ids] == record["orthogonal_rows_numerator"]
    assert {row.index(1) for row in matrix[:e]} == support
    assert {row.index(1) for row in matrix[e:]} == axes
    residuals[f] = axes
assert set(residuals) == {state["initial"][str(j)] for j in range(2 * V, LOCAL)}

# Reconstruct every host basis and every compressed stage route from geometry.
host_costs, host_coefficients, host_scales = [], [], []
geometry_costs, geometry_coefficients, geometry_scales = [], [], []
geometry_routes = 0
for port, data in enumerate(geo["ports"]):
    assert data["port"] == port and data["q"] == word["lines"][port]
    q = [Q(x, 2) for x in data["q"]]
    a = [[Q(x) for x in row] for row in data["complement_columns"]]
    assert len(a) == H and all(len(row) == 7 for row in a)
    b = [[q[i]] + a[i] for i in range(H)]
    assert multiply(transpose(b), b) == identity(H)
    cost, coefficients, scales = elementary_cost(b)
    host_costs.append(cost)
    host_coefficients += coefficients
    host_scales += scales
    p = [[q[i] * q[j] for j in range(H)] for i in range(H)]
    rho = [p[i] + a[i] for i in range(H)]
    rho += [list(column) + [Q(0)] * 7 for column in zip(*a)]
    assert rho == [[Q(x) for x in row] for row in data["rho15"]]
    assert transpose(rho) == rho and multiply(rho, rho) == identity(15)
    # P, FULL, ZERO, and K endpoint relations, with the exterior block active.
    for local in (p, identity(H), [[Q(0)] * H for _ in range(H)],
                  [[Q(i == j) - p[i][j] for j in range(H)] for i in range(H)]):
        source = [local[i] + [Q(0)] * 7 for i in range(H)]
        source += [[Q(0)] * H + row for row in identity(7)]
        target = multiply(multiply(rho, source), rho)
        top = identity(H) if local == p or local == identity(H) else [[Q(i == j) - p[i][j] for j in range(H)] for i in range(H)]
        bottom = identity(7) if local == identity(H) or local != p and local != [[Q(0)] * H for _ in range(H)] else [[Q(0)] * 7 for _ in range(7)]
        expected = [top[i] + [Q(0)] * 7 for i in range(H)]
        expected += [[Q(0)] * H + row for row in bottom]
        assert target == expected
    assert len(data["routes"]) == 11
    for stage, route in enumerate(data["routes"]):
        assert route["stage"] == stage
        if stage == 0:
            assert route == {"stage": 0, "axes": list(range(8)), "identity": True}
        else:
            assert route["axes"] == list(range(8)) + list(range(8 + 7 * (stage - 1), 8 + 7 * stage))
            reduced = [row[:] for row in rho]
            geometry_costs.append(len(route["elementary_inverse_replay"]))
            for kind, i, j, coefficient in route["elementary_inverse_replay"]:
                if kind == "swap":
                    assert coefficient is None
                    reduced[i], reduced[j] = reduced[j], reduced[i]
                elif kind == "scale":
                    geometry_coefficients.append(Q(coefficient))
                    geometry_scales.append(Q(coefficient))
                    reduced[i] = [Q(coefficient) * x for x in reduced[i]]
                else:
                    assert kind == "add"
                    geometry_coefficients.append(Q(coefficient))
                    reduced[i] = [x + Q(coefficient) * y for x, y in zip(reduced[i], reduced[j])]
            assert reduced == identity(15)
        geometry_routes += 1
assert max(geometry_costs) == geo["max_route_factors"]

idles = {e["idx"]: e for e in t["schedule"] if e["kind"] == "idle"}
slots = {}
for index, copy, offset, width, stage, helper in t["hosting"]["slots"]:
    assert (stage, helper) not in slots
    slots[stage, helper] = (index, copy, offset, width)
assert len(slots) == EXPECTED_HELPERS
counts, tags, route_costs = Counter(), Counter(), Counter()
verified_helpers = set()
mutation_controls = []
max_family_load = 0
assert len(t["calls"]) == 44
for call in t["calls"]:
    seen, load = defaultdict(set), Counter()
    owners = call["owners"]
    assert len(owners) == LOCAL
    for j, (family, route) in enumerate(owners[:240]):
        side = j // 120
        if call["orientation"] == "reverse":
            side = 1 - side
        assert family == call["replica"] * 1200 + (2 * call["pair"] + side) * 120 + j % 120
        assert route == ["data", call["stage"], j % 120]
    for j, (family, route) in enumerate(owners[240:], 240):
        key = (call["stage"], call["replica"], j)
        assert key not in verified_helpers
        verified_helpers.add(key)
        kind, index, offset, width, tag, encoded = route
        assert kind == "hosted" and type(tag) is int and 0 <= tag < 1024
        perm = tuple(map(int, encoded.split(",")))
        assert len(perm) == M and sorted(perm) == list(range(M))
        assert (index, offset, width) == tuple(slots[call["stage"], call["replica"] * R + j - 240][k] for k in (0, 2, 3))
        copy = slots[call["stage"], call["replica"] * R + j - 240][1]
        owner_replica, within = divmod(copy, 240)
        side, port = divmod(within, 120)
        idle = idles[index]
        assert family == owner_replica * 1200 + (2 * idle["pair"] + side) * 120 + port
        assert idle["pair"] != call["pair"]
        lo, hi = idle["source_level"], idle["target_level"]
        pending = list(range(1 if lo == -1 else 8 + 7 * lo, 8 + 7 * hi))
        assert len(pending) == idle["rank"]
        selected = pending[offset:offset + width]
        assert len(selected) == width
        residual = residuals[state["initial"][str(j)]]
        def valid_image(candidate):
            return len(residual) == width and {candidate[axis] for axis in residual} == set(selected)
        assert valid_image(perm)
        if not mutation_controls:
            bad = list(perm)
            inside, outside = min(residual), 8
            bad[inside], bad[outside] = bad[outside], bad[inside]
            assert sorted(bad) == list(range(M))
            assert not valid_image(bad)
            mutation_controls.append("A valid axis permutation with one residual axis moved outside its slot is rejected")
        signs = tuple(-1 if 8 <= axis < 18 and tag >> (axis - 8) & 1 else 1 for axis in range(M))
        assert signs[:8] == (1,) * 8 and signs[18:] == (1,) * 60
        normalized = tuple(signs[axis] * (perm[axis] + 1) for axis in range(M))
        assert normalized not in seen[family]
        seen[family].add(normalized)
        load[family] += 1
        cost = host_costs[port] + swap_cost(perm) + tag.bit_count()
        assert cost <= 144
        route_costs[cost] += 1
        tags[tag] += 1
        counts[width] += 1
    max_family_load = max(max_family_load, max(load.values()))
assert sum(counts.values()) == EXPECTED_HELPERS
assert verified_helpers == {(s, r, j) for s in range(11) for r in range(4) for j in range(2 * V, LOCAL)}
assert all(x.denominator & (x.denominator - 1) == 0 for x in host_coefficients + geometry_coefficients)
assert all(abs(x.numerator) & (abs(x.numerator) - 1) == 0 for x in host_scales + geometry_scales)
assert inputs == {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in PATHS}
result = dict(status="PASS_INDEPENDENT_EXACT_SIGNED_OWNER_ROUTES", inputs=inputs,
              helper_routes=sum(counts.values()), call_count=44, geometry_routes=geometry_routes,
              residual_frames=len(residuals), helper_widths=dict(sorted(counts.items())),
              sign_tags=dict(sorted(tags.items())), max_helpers_on_one_family_in_one_call=max_family_load,
              host_basis_factor_counts=dict(sorted(Counter(host_costs).items())),
              maximum_geometry_route_factors=max(geometry_costs),
              maximum_actual_route_factors=max(route_costs), charged_route_factors=144,
              host_coefficient_denominators=sorted({x.denominator for x in host_coefficients}),
              host_scale_numerator_magnitudes=sorted({abs(x.numerator) for x in host_scales}),
              mutation_controls=mutation_controls,
              exact_field_scope="Rational identities; injective owners over every admitted odd field",
              verification="Orthogonal host bases; signed-permutation routes; exported entrance complements; pending projector images; concrete per-call owner injection")
print(json.dumps(result, indent=2))
