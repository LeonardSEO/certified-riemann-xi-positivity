# Global cosine minorants compatible with moment integration

This note separates three questions that are easy to conflate:

1. Is the proposed function below `cos(r)` for every real `r`?
2. Can its expectation be computed or bounded from the available raw moments?
3. Does it change an all-orders positivity radius, rather than only a finite
   certificate?

The short answer is: fixed finite convex combinations and envelopes of Taylor
minorants can improve finite constants, but every fixed finite combination is
still a negative-leading polynomial and therefore has finite radius.  A
sequence of changing mixtures, or one infinite-support mixture, is a separate
problem; the finite search below does not settle it.  Any asymptotically
complete hierarchy whose radii diverge would recover global positivity of the
defect kernel and hence contains an RH-level limit.

## Reproduction

```sh
uv run --with python-flint==0.9.0 \
  python research/minorants/explore_minorants.py
```

The generated output is in `certificate.out`.  Arb evaluates endpoint moments
with outward-rounded balls.  It also certifies positivity up to each displayed
lower radius by a Bernstein-basis certificate and certifies a negative value at
the displayed upper radius.

## Baseline: why `T_(4m+2)` is globally valid

Let

```text
T_n(r) = sum_{j=0}^{n/2} (-1)^j r^(2j)/(2j)!,  n=4m+2.
```

For `g=cos-T_n`, one has `g^(n)=1-cos >= 0`, and all derivatives of
orders below `n` vanish at zero.  Repeated integration proves `g>=0` on the
positive half-line; evenness handles the negative half-line.  Strict inequality
holds away from zero.  This is an exact proof on all of `R`, with no tail
cutoff.

Among degree-`4m+2` polynomials having the same contact with cosine through
order `4m+2` at zero, there is no freedom: the polynomial is `T_(4m+2)`.
Improvement at the same degree must therefore sacrifice some local contact.

## Certified experiment

For the sign-safe cross-endpoint moment polynomial from the paper, extending
the Taylor order gives:

| degree | certified initial positivity radius |
|---:|---:|
| 2 | `[4.89087659, 4.89087664]` |
| 6 | `[6.14999148, 6.14999153]` |
| 10 | `[7.03624329, 7.03624334]` |
| 14 | `[7.46139709, 7.46139714]` |
| 18 | `[7.53283218, 7.53283223]` |
| 22 | `[7.53665519, 7.53665524]` |
| 26 | `[7.53676566, 7.53676571]` |
| 30 | `[7.53676778, 7.53676783]` |
| 34 through 50 | `[7.53676781, 7.53676786]` |

Thus higher Taylor minorants improve the degree-10 finite constant by about
`0.5005245`, but the computed radii rapidly saturate near `7.5367678`.  This is
strong executable evidence, not an all-orders proof of the limiting value.

The script also searches every pair of degrees through 50 with rational weights
in steps of `1/100`.  Convex combinations are exact global minorants.  The best
selected mixture does not improve the displayed eight-decimal radius.  The
search is finite and heuristic; validity and the selected radius bracket are
certified.

## Stronger constructions and what they require

### Convex combinations of Taylor minorants

For a fixed finite set of indices, if `lambda_k >= 0` and
`sum lambda_k=1`, then

```text
p(r) = sum lambda_k T_(4k+2)(r) <= cos(r)  for every real r.
```

Its expectation is a finite linear combination of raw even moments.  This is
the cleanest larger class compatible with the existing certificate.  Its
highest nonzero Taylor component has negative leading coefficient, so every
one such fixed mixture has finite initial radius.  The experiment only searched
pairwise mixtures through degree 50 on a `1/100` grid; it does not prove a
uniform radius bound over changing mixtures or infinite-support mixtures.

### Piecewise envelopes

The pointwise function

```text
max(-1, T_2(r), T_6(r), T_10(r), ...)
```

is a strictly stronger global minorant than any one entry.  The tail is
rigorous because `-1 <= cos(r)` globally.  However, integration introduces
terms such as

```text
E[Q^(2j) 1_{a < |xQ| <= b}],
```

which are truncated moments.  They are not determined by any fixed finite list
of raw moments.  Using the envelope without supplying certified truncated-mass
or tail information would therefore be an invalid strengthening of the paper's
moment argument.

A valid tail-aware route is possible: certify a polynomial/Chebyshev lower
approximation on `[-A,A]`, use `-1` outside, and separately certify truncated
moments or a tail law for the Riemann kernel.  That is new analytic input, not a
better use of the same endpoint moments.

### Chebyshev and SOS polynomials

On a compact interval, a shifted Chebyshev/minimax approximation can be made a
one-sided minorant by subtracting a rigorous uniform error.  An SOS or
Bernstein certificate can verify the resulting polynomial inequality there.
Global validity still needs a tail clause.  Two safe options are:

- a piecewise `-1` tail, which again needs truncated moments; or
- a negative-leading global polynomial penalty, which remains raw-moment
  compatible but spends higher moments to control the tail.

These methods may optimize a chosen finite radius.  They do not by themselves
give all-orders control.

### Rational minorants

A nonoscillatory rational function cannot mimic cosine's tail.  If a rational
minorant has a finite limit `L` at infinity, evaluation along odd multiples of
pi forces `L <= -1`.  Moreover, expectations of rational terms require
Stieltjes-type quantities such as `E[(1+aQ^2)^(-1)]`; a fixed list of raw
moments does not determine them.  Rational functions are therefore not directly
compatible with the current finite-moment certificate unless new transform
bounds are proved.

## The asymptotic boundary and the hidden RH-equivalent limit

There are two different hierarchies.

For the **exact moments at a fixed `y`**, the Taylor sections converge uniformly
on every compact `x`-interval (the kernel has exponential moments).  Therefore:

```text
the supremum of the initial positivity radii is infinite
iff C_y(x) > 0 for all real x (with the corresponding uniform-y formulation).
```

In the open-strip uniform formulation used by the paper, divergence supplies
global defect-kernel positivity and hence implies RH.  Calling an all-orders
Taylor, Chebyshev, SOS, rational, or piecewise hierarchy “stronger” does not
remove this limit: if it is asymptotically complete, proving its radii diverge
has simply repackaged the global positivity/RH step.

For the **cross-endpoint Taylor hierarchy**, positive and negative coefficients
use different pessimistic endpoint ratios, unattainable at one common `y`.
The mixed-limit argument in `mixed_limit_theorem.md` proves, for every fixed
`0 <= eps < 1/2`, that its limiting entire function tends to minus infinity and

```text
sup_m Rhat_m^(eps) < infinity.
```

Thus the degree-50 saturation near `7.5367678` reflects a genuine
unconditional finite-radius obstruction, although that calculation alone does
not certify the exact limiting radius.  This theorem concerns the individual
Taylor sequence.  It does not prove a uniform bound over all changing convex
mixtures.

## Conclusion

- `T_(4m+2)` remains the simplest exact all-real, finite-raw-moment minorant.
- Higher Taylor orders improve the certified degree-10 radius from about
  `7.03624` to about `7.53677`; the finite convex-mixture search found no
  further eight-decimal improvement.
- Piecewise/Chebyshev/SOS/rational improvements need truncated moments, tail
  bounds, transform bounds, or additional high moments.
- The individual cross-endpoint Taylor radii are proved uniformly bounded in
  their order for every fixed `eps<1/2`.  Every fixed finite convex mixture has
  finite radius.  Changing or infinite-support mixtures remain unclassified;
  if an asymptotically complete such hierarchy had diverging radii, it would
  reach the global-positivity barrier and, in the relevant uniform formulation,
  an RH-level assertion.
