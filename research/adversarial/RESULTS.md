# Adversarial audit results

Run date: 2026-07-20. Backend: `python-flint==0.9.0`, FLINT 3.6.0. Main scan:
384-bit Arb/Acb arithmetic, `0 <= m <= 12` (degrees 2 through 50).

## Explicit failures and counterexamples

1. **A fixed cap of 18 does not generalize beyond degree 14.** The required
   highest xi derivative for `Phat_m` is `4m+4`, so the minimal series cap is
   `4m+5`. For `m=4` (degree 18), cap 18 is already invalid; cap 21 is the
   minimum. The harness rejects this case instead of silently reading a
   missing coefficient. This is a concrete counterexample to reusing the
   degree-10 certificate's cap for a higher-degree hierarchy.

2. **Fixed precision is not uniform as epsilon tends to zero.** The interior
   identity `A_(2j)(epsilon)=-H'_(2j)(1/2-epsilon)/epsilon` incurs cancellation.
   At `m=6`, 128-bit precision, and `epsilon=10^-40`, all 14 moment balls fail
   to certify positivity. At 384 bits and `epsilon=10^-120`, all 14 fail. The
   `A_0` ball at the latter setting expands to approximately `0 +/- 8.87e6`.
   Thus any numerical claim uniform over all positive epsilon at one fixed
   precision is false. Precision must scale with `-log2(epsilon)`, or the
   endpoint must be evaluated with a regularized Taylor expansion.

3. **Low-degree radius growth is misleading.** For `epsilon=0`, the certified
   radii grow from 4.8908766132 (`m=0`) to 7.5367656891 (`m=6`), but then
   stabilize numerically:

   | m | degree | certified root (displayed center) |
   |---:|---:|---:|
   | 2 | 10 | 7.036243317590989 |
   | 4 | 18 | 7.532832204196342 |
   | 6 | 26 | 7.536765689065283 |
   | 8 | 34 | 7.536767836797394 |
   | 10 | 42 | 7.536767837085919 |
   | 12 | 50 | 7.536767837085932 |

   At `epsilon=1/1000`, `1/10`, and `1/4`, the degree-50 displayed roots are
   respectively 7.536770924308973, 7.568223683765071, and
   7.756317564535271. These finite computations do **not** disprove the
   all-orders statement, but they falsify an extrapolation that the first few
   increasing radii provide numerical evidence of divergence. The table is
   instead consistent with a finite limiting radius.

## Claims that survived this audit

- The independent degree-10 calculation reproduces
  `7.036243317590989...`, inside the paper's rational bracket.
- Minimal-cap and overprovisioned-cap moment balls overlap for every tested
  `m <= 12`.
- The direct double-Leibniz indexing and independent formal-series indexing
  overlap for the tested moments.
- Endpoint cross-normalization checks report no failures through `m=12`.
- Certified Acb isolation finds exactly one positive real root of `Q` and no
  positive real root of `Q'` for every tested combination of
  `m=0,...,12` and `epsilon in {0,1/1000,1/10,1/4}`. Hence uniqueness and
  strict decrease on `t>=0` survive this finite scan.
- Arb Horner evaluation remains finite at `x=10^100`; no machine overflow or
  enclosure loss occurs in that stress case at 384 bits.

## Scope

The failures above concern naive higher-degree/general-epsilon computation,
not the published finite degree-10 theorem. No counterexample to that finite
theorem was found. Root isolation and the plateau table are finite through
degree 50 and cannot establish or refute the paper's explicitly unproved
statement `sup_m Rhat_m^(epsilon)=infinity`.
