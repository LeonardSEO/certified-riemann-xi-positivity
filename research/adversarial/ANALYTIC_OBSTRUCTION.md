# Analytic obstruction to divergent cross-endpoint radii

## Verdict

Let `b=1/2`. For every fixed `0 <= a < b`, the cross-endpoint hierarchy
satisfies

```text
sup_m Rhat_m^(a) < infinity.
```

Thus the proposed missing assertion `sup_m Rhat_m^(epsilon)=infinity` is not
merely unproved: it is false for every `epsilon` strictly below `1/2`. This
includes every `epsilon` in the open-strip exhaustion intended in the paper.
The proof uses only positivity, strict raw-moment monotonicity, and the stated
exponential decay. It is independent of finite-precision computations.

## Reconstruction of the mixed limit

For fixed `y`, define the hyperbolic moment transform

```text
M_y(x) = integral W_y(u,v) cosh(x(u-v)) du dv
       = sum_(j>=0) A_(2j)(y) x^(2j)/(2j)!.
```

The decay assumption makes the series absolutely and locally uniformly
convergent. The cosine transform is

```text
C_y(x) = sum_(j>=0) (-1)^j A_(2j)(y) x^(2j)/(2j)!.
```

Consequently, the sums over even and odd values of the Taylor index `j` are

```text
E_y(x) = (M_y(x)+C_y(x))/2,
O_y(x) = (M_y(x)-C_y(x))/2.
```

The locally uniform limit of the cross-endpoint polynomials is therefore

```text
F_a(x)
 = 1 + (E_a(x)-A_0(a))/A_0(b) - O_b(x)/A_0(a)

 = 1 - A_0(a)/A_0(b)
   + 1/2 [M_a(x)/A_0(b) - M_b(x)/A_0(a)]
   + 1/2 [C_a(x)/A_0(b) + C_b(x)/A_0(a)].
```

The subtraction of `A_0(a)` is essential: the polynomial's constant term is
defined to be 1, rather than `L_0=A_0(a)/A_0(b)`.

## Why the limit is negative at large x

For `a<b`, pointwise monotonicity of `sinhc(yp)` gives

```text
W_b(u,v) >= W_a(u,v),
A_0(b) > A_0(a) > 0,
M_b(x) >= M_a(x).
```

Set

```text
delta = 1/A_0(a) - 1/A_0(b) > 0.
```

Then

```text
M_a(x)/A_0(b) - M_b(x)/A_0(a) <= -delta M_a(x).
```

Also `|C_y(x)| <= A_0(y)`, so the entire cosine part of `F_a` is bounded
above independently of `x`. On any positive-measure set where `|u-v|>=1`,
the weight `W_a` is positive except on a null line, and hence

```text
M_a(x) >= c cosh(x) -> infinity
```

for some `c>0`. It follows that

```text
F_a(x) -> -infinity as x -> +infinity.
```

Choose a finite `X` with `F_a(X)<0`. Local uniform convergence gives
`P_hat_m^(a)(X)<0` for every sufficiently large `m`.

## Passage from one negative value to the first positivity radius

Every `P_hat_m^(a)` has value 1 at zero. Its highest Taylor index is
`j=2m+1`, which is odd, so its leading coefficient is

```text
-U_(4m+2)^(a)/(4m+2)! < 0.
```

Thus every polynomial tends to `-infinity` and has a finite first positive
zero. Under any standard definition of initial positivity radius (the first
positive zero, or the supremum of the initial interval on which the
polynomial is positive), `P_hat_m^(a)(X)<0` implies

```text
Rhat_m^(a) <= X
```

for all sufficiently large `m`. The remaining values of `m` form a finite
set and each has a finite radius, proving the stated finite supremum.

## Endpoint and strictness checks

- **`a=0`:** The argument remains valid. `W_0=p^2 Phi(u)Phi(v)` is the
  continuous endpoint weight, its exponential moments are finite, and strict
  monotonicity gives `A_0(0)<A_0(1/2)`. No division by `a` occurs in this
  analytic proof.
- **`0<a<1/2`:** The same proof applies verbatim.
- **`a=1/2`:** The key number `delta` is zero. The mixed series collapses to
  the ordinary normalized cosine transform, so this obstruction does not
  decide its global positivity. The strict inequality `a<b` is indispensable.

## Computational issues versus the theorem

The fixed-cap and small-epsilon enclosure failures in the companion audit are
real defects in naive computations, but they do not weaken this theorem:

- the cap must grow with `m` to compute higher moments;
- direct evaluation of `-H'(1/2-a)/a` needs growing precision as `a->0`;
- neither issue appears in the integral inequalities above;
- the finite Arb plateaus are consistent with, but not needed for, the
  analytic conclusion.

Therefore increasing precision or repairing the series cap cannot restore
divergent cross-endpoint radii for any fixed `a<1/2`.
