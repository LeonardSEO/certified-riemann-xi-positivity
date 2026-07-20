# Independent high-degree endpoint study

This directory is an independent exploratory extension of the released
degree-10 certificate. It does not edit or import the released certificate.

Run a smoke test:

```bash
uv run --with python-flint==0.9.0 python research/high_degree/high_degree_endpoint_study.py \
  --m 0 1 2 --eps 0 1/4 --dps 100 --output research/high_degree/smoke.jsonl
```

Run the full experiment:

```bash
/usr/bin/time -l uv run --with python-flint==0.9.0 \
  python research/high_degree/high_degree_endpoint_study.py \
  --m 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 25 30 40 50 \
  --eps 0 1/4 1/8 1/16 1/32 1e-2 1e-3 \
  --dps 700 --bisect-bits 120 \
  --output research/high_degree/full_dps700.jsonl
```

Each `case` record keeps `certified` Arb results separate from `ordinary`
binary64 midpoint diagnostics. A radius is certified as the *first* positive
root only when interval Horner evaluation proves the derivative strictly
negative from zero through the root bracket.

The successful full run needed 700 decimal digits. The retained 180-digit
attempt shows why: cancellation makes `A_120(1/2)` indeterminate at that
precision. See `SUMMARY.md` for results and the 900-digit cross-check.
