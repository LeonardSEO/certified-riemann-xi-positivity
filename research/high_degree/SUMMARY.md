# High-degree endpoint-moment study: results

## Scope and outcome

The Arb run evaluated all 816 requested endpoint moments (102 moments at each
of `epsilon = 1/2, 0, 1/4, 1/8, 1/16, 1/32, 1e-2, 1e-3`) and all 175 requested
polynomials (`m = 0..20, 25, 30, 40, 50`). The largest polynomial has degree
202 in `x`. Every 700-decimal-digit case has a certified sign-changing dyadic
bracket for its first positive root and an interval-Horner proof that the
polynomial is strictly decreasing from zero through that bracket. There were
no failures in the 700-digit run.

This is finite computational evidence only. The radii quickly approach a
finite-looking value in this tested range; these calculations do not establish
the all-orders divergence needed by the paper's open condition.

## Degree-202 radii

The following displayed digits are taken from the lower endpoint of the
900-digit Arb enclosure. The exact certified results are the dyadic `t=x^2`
brackets in `crosscheck_m50_dps900.jsonl`.

| epsilon | certified lower endpoint for R_50 |
|---:|---:|
| 0 | 7.536767837085931785139... |
| 1/4 | 7.756317564535271286279... |
| 1/8 | 7.586452284709565698410... |
| 1/16 | 7.548914923909536812700... |
| 1/32 | 7.539788134079186543997... |
| 1e-2 | 7.537076615696515414308... |
| 1e-3 | 7.536770924308972954077... |

The 900-digit, 140-bisection-bit intervals are contained in the corresponding
700-digit, 120-bit intervals for all seven epsilon values. Their widths in
`t` are about `4.59e-41`; the full-run widths are about `4.81e-35`.

The certified radius brackets strictly increase through every adjacent
requested value from `m=0` through `m=20`, then from `20` to `25`, and from
`25` to `30`. At 240 bisection bits, changes from `m=30` to `40` and `40` to
`50` are too small to order (bracket width about `3.62e-71`); no equality or
monotonicity claim is made for those two comparisons. This is separate from
the polynomial-in-`x` monotonicity: strict decrease before the first root was
certified in every one of the 175 cases.

## Certified versus ordinary results

- `certified`: Arb ball moment arithmetic, rational-dyadic root endpoints,
  outward-rounded sign tests, and adaptive interval-Horner derivative bounds.
- `ordinary`: binary64 evaluation of Arb coefficient midpoints followed by a
  sign search and bisection. It is diagnostic only. At degree 202 its last few
  displayed digits can disagree with the certified enclosure, demonstrating
  the conditioning problem; it is never used by a certificate assertion.

## Precision, order, runtime, and memory

- Failed exploratory run: 180 decimal digits, series cap 205. Positivity first
  became indeterminate at `A_120(1/2) = [+/- 8.40e+21]`. Runtime 0.25 s;
  maximum resident set size 37,109,760 bytes. The partial output and traceback
  are retained as `full_dps180.jsonl` and `full_dps180.time.txt`.
- Successful full run: 700 decimal digits (2329 bits), series cap 205,
  moments through order 202, 120 root-bisection bits. Internal runtime 3.00 s;
  externally measured wall time 3.74 s; maximum resident set size 41,058,304
  bytes.
- Degree-202 cross-check: 900 decimal digits, series cap 205, 140 bisection
  bits. Internal runtime 3.29 s; wall time 3.49 s; maximum resident set size
  44,744,704 bytes.
- Tail ordering run: 900 decimal digits and 240 bisection bits for
  `m=19,20,25,30,40,50`. Internal runtime 3.73 s; maximum resident set size
  45,826,048 bytes.

Environment: Python 3.12.11 under `uv`, python-flint 0.9.0, FLINT 3.6.0.

## Verification

Run from the repository root:

```bash
python3 research/high_degree/verify_results.py
```

Expected output:

```text
PASS: 175 certified cases, 816 endpoint moments, dps900 containment, tail increases through m=30
```

See `README.md` for exact recomputation commands. SHA-256 hashes for the code
and result artifacts are in `SHA256SUMS`.
