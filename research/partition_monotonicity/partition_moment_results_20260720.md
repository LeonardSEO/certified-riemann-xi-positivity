# Local y-partitions and normalized moments (2026-07-20)

This note records a separate Arb experiment.  It does not modify or extend the
paper's stated theorem, and it does not prove an all-orders assertion.

## 1. Exact covariance identity

Put `F_j(u,v)=(u-v)^(2j)` and let `mu_y` be the probability measure with
density `W_y/A_0(y)`.  Absolute/local-uniform convergence from the kernel's
double-exponential decay permits differentiation under the integral.  For
`y>0`,

```text
g_y(p) = d/dy log(sinhc(yp)) = p*coth(yp) - 1/y,
m_(2j)'(y) = Cov_{mu_y}(F_j, g_y(p)).
```

This is the standard derivative-of-a-normalized-integral identity: both the
numerator and normalizer acquire the same score, and the quotient rule
subtracts their product of expectations.  The score extends asymptotically as

```text
g_y(p) = y*p^2/3 - y^3*p^4/45 + O(y^5*p^6),
m_(2j)'(0)=0,
lim_{y->0+} m_(2j)'(y)/y = Cov_{mu_0}(F_j,p^2)/3.
```

For fixed `y>0`, `g_y(p)` is even and strictly increasing in `|p|`, because,
with `t=y|p|>0`,

```text
d/d|p| g_y(p) = coth(t)-t*csch(t)^2
                = (sinh(2t)-2t)/(2*sinh(t)^2) > 0.
```

That monotonicity does **not** determine the covariance sign: `F_j` depends on
`q=u-v`, whereas the score depends on `p=u+v`.  A negative-association theorem
for this particular transformed Riemann density would still be needed for an
all-`j` analytic proof.

## 2. Certified finite-order result

Let `h_j(y)=H_(2j)(1/2-y)`.  Since

```text
A_(2j)(y)=h_j'(y)/y,
m_(2j)(y)=h_j'(y)/h_0'(y)       (y>0),
```

the sign of `m_(2j)'` is the sign of

```text
N_j(y)=h_j''(y)h_0'(y)-h_j'(y)h_0''(y).
```

The companion program gives a proof by outward-rounded Arb balls:

- a Taylor-remainder enclosure proves `m_(2j)'(y)/y<0` on `0<y<=0.01`;
- 1000 exact rational cells cover `[0.01,0.5]`;
- on each cell the program forms `N_j` before interval evaluation, then uses a
  degree-11 Taylor polynomial plus an interval enclosure of the 12th
  derivative for the remainder;
- every complete ball for `h_0'` is positive and every complete ball for
  `N_j`, `j=1,...,6`, is negative.

Therefore the certificate proves:

> For each `j=1,...,6`, `m_(2j)` is even in `y` and strictly decreasing on
> `(0,1/2]`.  On `[0,1/2]` it is consequently unimodal, with its unique maximum
> at `y=0` and minimum at `y=1/2`.

The least-negative upper bounds among all 1000 positive-cell numerator balls
were:

| moment | max cell upper bound for `N_j` |
|---|---:|
| `m_2` | `-3.5009258492825374e-13` |
| `m_4` | `-1.5511474707812203e-13` |
| `m_6` | `-8.464782094508236e-14` |
| `m_8` | `-5.660830435544368e-14` |
| `m_10` | `-4.492080805022067e-14` |
| `m_12` | `-4.116455929704137e-14` |

The same run gives the following complete Arb balls at `y=0`:

| moment | `(log m_(2j))''(0)` (ball center shown; radii below `6e-58`) |
|---|---:|
| `m_2` | `-0.0081385916943803848475757658427961492812300` |
| `m_4` | `-0.0148276396841586132505807261112511797686952` |
| `m_6` | `-0.0203950698658259948560367043311742525570618` |
| `m_8` | `-0.0250883556493556965206940711583138525437092` |
| `m_10` | `-0.0290933742199584401647238165773346134780491` |
| `m_12` | `-0.0325501170092364643094743475574431574720445` |

Thus log-convexity in `y` is rigorously false already for `m_2` (and for all
six tested normalized moments).  This is a certified counterexample to the
proposed shape property, not merely a plotted sign.

## 3. What local partitions do in the mesh limit

Fix `epsilon>=0` and a partition
`P: epsilon=a_0<a_1<...<a_N=1/2`.  On the cell `I_i=[a_i,a_(i+1)]`, strict raw
moment monotonicity supplies

```text
L_(2j,i)=A_(2j)(a_i)/A_0(a_(i+1)) < m_(2j)(y)
          < A_(2j)(a_(i+1))/A_0(a_i)=U_(2j,i).
```

Use `L` for positive Taylor terms and `U` for negative Taylor terms to obtain
the local lower polynomial `P_hat_(m,i)`.  Two conclusions are distinct.

1. **Every fixed nondegenerate cell retains the endpoint obstruction.**
   Its lower and upper values use incompatible endpoints and are strictly
   separated.  Subdividing into finitely many fixed positive-width cells can
   reduce this mismatch but does not remove its all-orders tail obstruction
   on any such cell.

2. **Mesh tending to zero removes only that artificial mismatch at each fixed
   Taylor order.**  On a compact y-interval, every `A_(2j)` is positive and
   uniformly continuous.  Hence, for fixed `m`, `L_(2j,i)` and `U_(2j,i)`
   converge uniformly to `m_(2j)(y)` as `mesh(P)->0`.  Consequently the
   piecewise local lower polynomials converge uniformly on bounded x-ranges to
   the exact section

   ```text
   S_m(y,x)=sum_{j=0}^{2m+1} (-1)^j m_(2j)(y)x^(2j)/(2j)!.
   ```

The order of limits matters.  Refining the mesh with `m` fixed yields only the
fixed exact Taylor section, not positivity for unbounded `x`.  If one imposes
a joint/diagonal condition strong enough that, for every finite `R` and every
compact `epsilon<=y<=1/2`, some sufficiently fine partition and sufficiently
large `m` make all local lower polynomials positive on `|x|<=R`, then the exact
Taylor hierarchy shows this is equivalent to

```text
C_y(x)>0 for all real x and epsilon<=y<=1/2.
```

Letting `epsilon->0+` gives global **open-strip** strict defect positivity, and
this is RH-equivalent.  One direction is the zero contradiction from the
defect identity.  Conversely, under RH the canonical product for `Xi` has only
real zeros, so for `y>0`

```text
Im(Xi'(x+iy)/Xi(x+iy))
  = -sum_r multiplicity(r)*y/((x-r)^2+y^2) < 0,
```

with the usual real exponential/product terms contributing no imaginary
part.  The defect is `-4|Xi|^2 Im(Xi'/Xi)>0`.  Multiplicity does not spoil the
open-strip inequality.

There is one boundary nuance.  If the limiting condition additionally demands
strict positivity at `y=0` for every real `x`, then it is stronger than bare
RH: at a real Xi-zero, `C_0(x)=2 Xi'(x)^2`, so a multiple zero gives equality.
Thus the honest classification is: open-strip zero-mesh/all-orders positivity
is RH-equivalent; closed-strip strict positivity also encodes simplicity.  In
neither reading does the limit produce a new strictly intermediate theorem.

## 4. Reproduction

From the repository root:

```bash
uv run --with python-flint==0.9.0 \
  python research/partition_monotonicity/partition_moment_certificate_20260720.py \
  --cells 1000 --moments 6 --dps 80
```

The final line must be:

```text
ALL PARTITION MOMENT CERTIFICATE ASSERTIONS PASSED
```

Do not use Python optimization (`-O`), because assertions are load-bearing.
