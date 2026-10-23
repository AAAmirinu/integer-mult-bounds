# Validation

Source base: `1ec1119972c9aefe42525172d07b332fcff81cb4`.
Scientific interpreter: CPython 3.12.13, macOS arm64, standard library.

Completed during construction:

```sh
python3.12 -B research/native-gauge-cancellation/verify.py --write
```

Result: `PASS_NATIVE_GAUGE_CANCELLATION_NO_KAPPA_CHANGE`.
This authoring run generated RESULT.json and ran both retained interpreters,
full local invoice checks and semantic controls. Further publication checks
are recorded below after execution. Hosted CI is not yet claimed.

Publication checks completed before the first commit:

```sh
python3.12 -B scripts/research_package.py --package research/native-gauge-cancellation
python3.12 -I -O -B research/native-gauge-cancellation/verify.py
```

Both pass. The registered command reports
`PASS_REGISTERED_RESEARCH_PACKAGE research/native-gauge-cancellation outcome=completed`.
The initial isolated run could not import the local constructor. The verifier
now loads it by its explicit file path; the isolated and registered commands
above both passed after that correction. No scientific receipt changed.
