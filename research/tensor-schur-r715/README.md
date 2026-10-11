# Conditional kappa = 0.001291542455423938

Two-layer target interval factoring on pinned PR470, with our PR471 complex supplier. Improvement:0.1460538996 percent over PR470, within the whole-owner construction. This is not a claim to exceed larger cross-family claims with different admission assumptions.

Run from the repository root:

    python -B research/tensor-schur-r715/verify.py /absolute/new/output

Requires Python3.11+, SymPy, a C++17 compiler and Boost headers. Set CXX and BOOST_INCLUDE if needed. No network, optimizer or Lean is required for replay. Use a new output directory outside the package. Do not disable Python assertions.

PROOF.md gives the exact construction and scope. PROVENANCE.md records direct reuse; PR.md contains the ASCII-only title and pull-request statement. RESULT.json and EXPECTED.json contain exact rational results. VALIDATION.json distinguishes the checks actually run. All inherited all-size compiler, hosting and analytic interfaces remain conditional.
