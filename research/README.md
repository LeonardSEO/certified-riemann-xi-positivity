# Higher-degree endpoint-moment investigation

## Principal classification: E — cross-endpoint route blocked

For the cross-endpoint polynomials specified in the research question, the
certified radii cannot tend to infinity.  More precisely, the following
unconditional theorem holds.

### Theorem (fixed endpoint mismatch forces bounded radii)

For every fixed `0 <= epsilon < 1/2`,

```text
sup_m Rhat_m^(epsilon) < infinity.
```

This theorem uses neither RH nor any assertion about zeta zeros.  It blocks
the fixed-width cross-endpoint hierarchy, not RH and not every possible local
partition hierarchy.

### Proof

Write `p=u+v`, `q=u-v`, and let `mu_y` be the positive measure with density
`W_y`.  Put

```text
a = A_0(epsilon),       b = A_0(1/2),
G_y(x) = C_y(i x) = integral cosh(x q) d mu_y.
```

The theta-kernel decay gives every exponential `q`-moment, so the moment
series for `C_y` and `G_y` converge absolutely and locally uniformly on the
complex plane.  Splitting the moment index `j` by parity gives

```text
sum_(j even) A_(2j)(y) x^(2j)/(2j)! = (G_y(x)+C_y(x))/2,
sum_(j odd)  A_(2j)(y) x^(2j)/(2j)! = (G_y(x)-C_y(x))/2.
```

The positive even sum in `P_hat_m` omits `j=0`.  Consequently its exact
locally uniform limit is

```text
F_epsilon(x)
 = 1-a/b
   +(G_epsilon(x)+C_epsilon(x))/(2b)
   -(G_(1/2)(x)-C_(1/2)(x))/(2a).
```

For `epsilon<1/2`, strict increase of `sinhc(y p)` in `y` away from `p=0`
implies

```text
0 < a < b,       W_(1/2) >= W_epsilon,
G_(1/2)(x) >= G_epsilon(x).
```

Positivity of the measure gives `|C_y(x)| <= A_0(y)`.  Hence

```text
F_epsilon(x)
 <= 1-a/b+a/(2b)+b/(2a)
    -(b-a) G_epsilon(x)/(2ab).
```

The measure `mu_epsilon` has positive mass on a compact set where
`|q|>=delta>0`.  Therefore

```text
G_epsilon(x) >= c cosh(delta x) -> infinity,
```

and `F_epsilon(x)->-infinity`.  Choose `X` with `F_epsilon(X)<0`.
Local uniform convergence gives `P_hat_m(X)<0` for all sufficiently large
`m`, so their initial positivity radii are at most `X`.  Every exceptional
finite-degree polynomial also has a finite first positive zero: its value at
zero is one and its leading coefficient (index `j=2m+1`) is negative.  The
finite maximum of those exceptional radii and `X` proves the theorem.

The proof deliberately excludes `epsilon=1/2`.  There `a=b`, the coercive
cosh coefficient vanishes, and the limiting function is the exact normalized
cosine transform.  The bound obtained above is not uniform as
`epsilon` approaches `1/2`.

## Certified computation

The independent Arb implementation computed moments through `A_202` and all
175 requested cases:

```text
m = 0,...,20,25,30,40,50
epsilon = 0, 1/4, 1/8, 1/16, 1/32, 1e-2, 1e-3.
```

Every successful case contains an exact dyadic root bracket and an
interval-Horner certificate that the polynomial is strictly decreasing up to
that first root.  The complete per-case degree, bracket, precision, runtime,
memory, derivative order, monotonicity result, and failure field are in
`high_degree/full_dps700.jsonl`.  A 900-decimal-digit rerun of the degree-202
cases is enclosed in the 700-digit results.

Certified lower endpoints at `m=50` are:

| epsilon | lower endpoint for R_50 |
|---:|---:|
| 0 | 7.536767837085931785139... |
| 1/4 | 7.756317564535271286279... |
| 1/8 | 7.586452284709565698410... |
| 1/16 | 7.548914923909536812700... |
| 1/32 | 7.539788134079186543997... |
| 1e-2 | 7.537076615696515414308... |
| 1e-3 | 7.536770924308972954077... |

These numbers are finite certificates, not the proof of boundedness.  The
analytic theorem above supplies the all-orders conclusion.

The retained 180-digit run fails at `A_120(1/2)` with an indeterminate ball.
The successful full run used 700 decimal digits (2329 bits), series cap 205,
120 root-bisection bits, 3.74 seconds wall time, and about 41.1 MB maximum
resident memory.  The 900-digit degree-202 cross-check used about 44.7 MB.

## Other rigorous findings

- A structurally independent clean-room certificate reproduces the degree-10
  endpoint moments, all normalization factors, strict boundary positivity,
  and `7.0362433 < R_10 < 7.0362434`.
- For every `m>=0`, the Taylor polynomial `T_(4m+2)` is a strict global
  minorant of cosine away from zero.  This follows by integrating
  `1-cos(t)` exactly `4m+2` times.
- Arb proves that `m_2,m_4,...,m_12` are strictly decreasing on
  `[0,1/2]`.  This is finite order only.
- Log-convexity in `y` is false: already
  `(log m_2)''(0)=-0.0081385916943803848...<0`.
- Every fixed positive-width local partition cell has the same endpoint
  mismatch obstruction.  Mesh refinement at fixed degree merely approaches
  the exact Taylor section.  A diagonal scheme quantified over every compact
  open strip and every finite `x`-range is equivalent to global open-strip
  defect positivity and hence to RH; it is not an intermediate theorem.
- The formal high-moment saddle calculation predicts opposite-tail saddles
  near `p=0`, `q=+/-W(j/pi)`, but explicit uniform remainder constants were
  not completed.  No final theorem depends on that calculation.

## Reproduction

Install the pinned wrapper through `uv`, then run:

```bash
uv run --with python-flint==0.9.0 python research/cleanroom/independent_xi_moment_arb.py
uv run --with python-flint==0.9.0 python research/high_degree/verify_results.py
PYTHONPATH=research/adversarial uv run --with python-flint==0.9.0 \
  python -m unittest -v research/adversarial/test_adversarial.py
uv run --with python-flint==0.9.0 python research/minorants/explore_minorants.py
uv run --with python-flint==0.9.0 \
  python research/partition_monotonicity/partition_moment_certificate_20260720.py \
  --cells 1000 --moments 6 --dps 80
```

The large result files have their own hashes in
`high_degree/SHA256SUMS`.  Run that check from the `high_degree` directory.

## Eight-round status registry

1. Clean-room identities and degree-10 reconstruction: passed.
2. Degree-202 Arb computation plus independent codebase: passed; one retained
   insufficient-precision failure.
3. Normalized moments and local partitions: finite decreasing-moment theorem
   proved; log-convexity refuted; fixed-cell obstruction proved.
4. Uniform saddle analysis: leading formal saddle identified; explicit-error
   theorem incomplete and excluded from dependencies.
5. Root asymptotics: mixed cosine/cosh limit gives unconditional boundedness.
6. Alternative global minorants: finite improvements only; fixed finite
   convex combinations have finite radii; changing infinite hierarchies remain
   unclassified unless they collapse to RH-level positivity.
7. Five independent reconstructions plus convergence and circularity audits:
   boundedness theorem passed after correcting the mandatory `-a/b` term.
8. Central reruns, artifact hashes, dependency audit, and classification:
   see the verification output below.

## Exact scope

This investigation proves no new zero-free region and no statement about the
truth or falsity of RH.  It proves that the particular fixed cross-endpoint
lower-polynomial mechanism cannot yield unbounded positivity bands.  Local
partitioning remains useful for finite constants, but its fully refined
all-orders limit is an RH-equivalent exact criterion rather than an
independently established scalable mechanism.
