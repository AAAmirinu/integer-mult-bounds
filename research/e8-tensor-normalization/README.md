# Full-footprint tensor normalization with borrowed identity spectators

Conditional composed exponent: **Îº = 1274548075945587 / 10^18 = 0.001274548075945587**.

This improves the frozen PR456 reference 0.001266564732900111 by **0.6303146486%**. The snapshot was frozen through PR457; this is not a claim about later submissions. The bit supplier now binds.

| Component | Exact certified lower saving |
|---|---:|
| Bit: PR457 rank151 + PR450 target mixing + reused two-prefix recovery | 0.001276174621854442560268 |
| Complex: PR449 kernel79 + full nine-axis normalization + borrowed spectators | 0.001305231506267591 |

Two additions make the complex gain possible: exact two-sided Gaussian monomial wrappers around complete dirty-helper invocations, and borrowing their inactive ninth coordinate from outside a pending child in the SAME physical array. Every helper still has a full nine-axis physical footprint. These mechanisms admit the existing public kernel; the kernel itself is not claimed as new.

The final complex witness uses77 complete calls, 43,120 whole helper occurrences, and 6,083 borrowed spectators. Its live stock is 8,400 and physical stock 8,978, ambient dimension 89, rank mass 744,744, and deficit 2,856. Paidprofile:

```text
{1:153851,2:71764,3:4807,4:17248,5:33266,
 6:2,7:2254,8:6356,40:1,64:2046}
```

## Reproduce

From the repository root:

```sh
python -B research/e8-tensor-normalization/verify.py /fresh/output/directory
```

Requires Python 3.11+, SymPy, a C++17 compiler and Boost headers. Set `CXX` and `BOOST_INCLUDE` if they are not discoverable; the latter names the directory containing `boost/`. The output directory must not exist and must be outside the package. Do not run Python with `-O`. No network, optimizer or Lean installation is needed. Allow several minutes; generated outputs need tens of MB.

The verifier rebuilds the changed bit checks, regenerates the complex scalar/phase/wrapper certificates, independently replays owner routes and paid complements, expands the complete controller, and checks the finite invoices, both rational moment implementations and all 47 strict outer constraints. The adjacent kappa grid point must be rejected.

## Scope

This is a conditional multiplication-bound research artifact under the inherited all-size supplier/hosting/compiler and outer-assembly interfaces. It is not an unconditional proof that integer multiplication beats n log n, not a new Lean certification, and not a claim that all public PRs were independently replayed. Frozen baseline controller/phase material is source-bound; the changed construction is replayed explicitly. Source-only P18/TI retrieval supplied structural inspiration, not a substitute certificate.

See PROOF.md for the sufficient operator/storage argument, PROVENANCE.md for direct PR credit and actual tensor-source lineage, RESEARCH.md for failed screens and future routes, and PR.md for the proposed submission text. Upstream copyright and license notices are retained. Nothing in this folder uploads or publishes anything.

Upstream scalar-audit receipts retain their original provisional scope labels. The top-level validation separately checks the new normalization, physical admission, controller and invoice; a local scalar receipt alone is not the final certificate.
