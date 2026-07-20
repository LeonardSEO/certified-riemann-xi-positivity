# Mixed-limit theorem for the cross-endpoint hierarchy

This reconstruction starts from the definitions and does not use the numerical
radius experiment.

Fix `0 <= eps < 1/2` and abbreviate

```text
a = A_0(eps),       b = A_0(1/2),       so 0 < a < b,
L_(2j) = A_(2j)(eps)/b,
U_(2j) = A_(2j)(1/2)/a.
```

Raw-moment monotonicity gives both strict inequalities.  The cross-endpoint
polynomial is

```text
Q_m(x) = 1
       + sum_{1 <= j <= 2m+1, j even} L_(2j) x^(2j)/(2j)!
       - sum_{1 <= j <= 2m+1, j odd } U_(2j) x^(2j)/(2j)!.
```

Its degree is `4m+2`, not `4m+4`, and its leading coefficient is negative.

## Exact mixed-limit formula

For real or complex `z`, write

```text
C_y(z) = sum_{j >= 0} (-1)^j A_(2j)(y) z^(2j)/(2j)!.
```

The theta kernel has exponential moments of every order (indeed substantially
faster decay), so this series is entire and converges absolutely and uniformly
on every compact subset of the `z`-plane.  In particular,

```text
C_y(i x) = sum_{j >= 0} A_(2j)(y) x^(2j)/(2j)!.
```

Separating even and odd values of the moment index `j` gives

```text
sum_{j even} A_(2j)(y) x^(2j)/(2j)! = (C_y(x)+C_y(i x))/2,
sum_{j odd } A_(2j)(y) x^(2j)/(2j)! = (C_y(i x)-C_y(x))/2.
```

The `j=0` term in the first identity is `A_0(eps)/b`, whereas `Q_m`
has constant term one.  Therefore the locally uniform limit is exactly

```text
Q_inf^(eps)(x)
 = 1 - a/b
   + (C_eps(x)+C_eps(i x))/(2b)
   + (C_(1/2)(x)-C_(1/2)(i x))/(2a).                 (1)
```

The correction `1-a/b` is essential.  Omitting it is a constant-term error.
The signs of both imaginary-axis terms are also essential: the `eps` term is
positive and the `1/2` term negative.

## The mixed limit tends to minus infinity

For real `x`, positivity of the defining measure gives

```text
|C_y(x)| <= A_0(y).
```

It also gives

```text
C_y(i x) = integral W_y(u,v) cosh(x(u-v)) du dv >= 0.
```

Since `W_y` contains `sinhc(y(u+v))` and this factor increases with `y>=0`,

```text
C_(1/2)(i x) >= C_eps(i x).                           (2)
```

Using (2) in (1),

```text
Q_inf^(eps)(x)
 <= 1-a/b + a/(2b) + b/(2a)
    - (1/(2a)-1/(2b)) C_eps(i x).                     (3)
```

The coefficient in the last line is strictly positive because `a<b`.
Furthermore `C_eps(i x) -> +infinity`: the positive measure assigns positive
mass to a set where `|u-v| >= delta` for some `delta>0`, and on that set
`cosh(x(u-v)) >= cosh(delta x)`.  Hence (3) proves

```text
Q_inf^(eps)(x) -> -infinity as |x| -> infinity.       (4)
```

This proof is unconditional and works for every fixed `eps<1/2`.  It fails
exactly at `eps=1/2`, where `a=b` and the coercive coefficient vanishes.

## Uniform boundedness of the Taylor radii

Let `Rhat_m^(eps)` be the initial radius on which `Q_m` is positive.  By local
uniform convergence, choose a finite `x_*` with `Q_inf^(eps)(x_*)<0`; then

```text
Q_m(x_*) < 0
```

for every sufficiently large `m`.  Thus `Rhat_m^(eps) <= x_*` for all such
`m`.  Each of the finitely many remaining polynomials has finite initial
radius because it starts at one and has negative leading coefficient.  Hence

```text
sup_{m >= 0} Rhat_m^(eps) < infinity
for every fixed 0 <= eps < 1/2.                       (5)
```

So the proposed cross-endpoint condition saying that this supremum is infinite
for every positive `eps` is not merely unproved: with these definitions it is
false.

There is no contradiction with the exact-moment hierarchy.  The mixed
polynomial combines positive coefficients from `y=eps` with negative
coefficients from `y=1/2`, and divides them by opposite endpoint masses.  No
single value of `y` realizes this coefficient sequence.

## Convex combinations of Taylor minorants

Let a fixed finite convex combination of global Taylor minorants be

```text
p(r) = sum_k lambda_k T_(4k+2)(r),
lambda_k >= 0, sum_k lambda_k=1.
```

It is a global cosine minorant.  Applying the same fixed cross-endpoint bounds
produces exactly

```text
Q_lambda(x) = sum_k lambda_k Q_k(x).
```

This is a polynomial whose highest nonzero Taylor component has negative
leading coefficient.  Therefore every fixed finite convex combination also
has a finite initial positivity radius.  It cannot turn (5) into an individual
all-real positive lower bound.

One must distinguish this from the stronger assertion that the radii are
uniformly bounded over *all changing convex combinations with unbounded
support*.  Equation (5) alone does not prove that assertion: initial positivity
radius is not a convex functional, and two polynomials can in general cover
one another's negative regions.  A proof would require a common negative
evaluation/positive linear functional for every `Q_m`, or additional shape
control.  The finite pairwise search in `explore_minorants.py` is evidence, not
such a theorem.

If a sequence of changing convex combinations did have radii tending to
infinity, the resulting lower bounds would directly prove defect-kernel
positivity on every finite interval.  Requiring this uniformly as `eps` ranges
over the open strip recovers the same global-positivity/RH barrier.  Thus
convexification does not evade the hidden RH-level obstruction; but a blanket
uniform bound over every possible changing mixture should not be claimed from
the mixed-limit argument alone.

## Audited points

- Constant correction: `1-A_0(eps)/A_0(1/2)`.
- Positive terms: even moment index `j`, powers divisible by four.
- Negative terms: odd moment index `j`, powers congruent to two modulo four.
- Degree: `4m+2`, with negative leading coefficient.
- Convergence: entire in `x`, locally uniform on all of `C`, from exponential
  moments of every order.
- Endpoint exception: the proof of coercivity requires `eps<1/2`.

