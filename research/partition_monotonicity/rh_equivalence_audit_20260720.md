# Circularity audit: partition limit versus RH

## Verdict

The classification is correct with explicit quantifiers:

- positivity of the zero-mesh/all-orders limit on every compact substrip
  `epsilon <= y <= 1/2`, `epsilon>0`, and every bounded x-interval is
  equivalent to RH;
- requiring strict positivity also on the boundary `y=0` is equivalent to RH
  plus simplicity of all nontrivial zeros;
- no finite partition, finite moment order, mesh-convergence statement at a
  fixed order, or observed moment monotonicity proves either global condition.

## Canonical-product check

Under RH, `Xi` is a real even entire function of order one whose zeros are the
real numbers `+/- gamma`, counted with multiplicity.  Pairing opposite zeros
gives the locally uniformly convergent product

```text
Xi(z)=Xi(0) product_(gamma>0) (1-z^2/gamma^2)^(multiplicity(gamma)).
```

The paired product is legitimate because the Riemann-zero counting estimate
implies `sum gamma^(-2)<infinity`.  A possible order-one exponential factor is
constant: real-entire symmetry makes its coefficient real and evenness forces
that coefficient to vanish.  Thus, off the zeros,

```text
Xi'(z)/Xi(z)
 = sum_(gamma>0) multiplicity(gamma)
   * (1/(z-gamma)+1/(z+gamma)).
```

For `z=x+iy`, `y>0`, every summand has strictly negative imaginary part.  The
series may be differentiated/log-differentiated locally uniformly after
pairing, again by `sum gamma^(-2)<infinity`.  Hence

```text
Im(Xi'(z)/Xi(z)) < 0.
```

RH puts no Xi-zero in the upper half-plane, so multiplication by `|Xi(z)|^2`
is harmless.  The exact defect identity becomes

```text
2y C_y(x) = -4 |Xi(z)|^2 Im(Xi'(z)/Xi(z)) > 0.
```

This proves the RH-to-open-strip direction without assuming simple zeros.
Conversely, strict `C_y(x)>0` for `0<y<1/2` excludes any zero off the critical
line: a nontrivial zero has `0<Re rho<1`, so its reflected Xi-zero has an
imaginary part strictly between zero and `1/2`, where the defect would vanish.

At `y=0`, the paired log derivative gives the real Laguerre inequality

```text
(Xi')^2-Xi Xi''
 = Xi(x)^2 sum_r multiplicity(r)/(x-r)^2 > 0
```

away from zeros.  At a real zero `r`, the paper's identity gives
`C_0(r)=2 Xi'(r)^2`, which is positive exactly when that zero is simple.
Therefore strict closed-boundary positivity is RH plus simplicity, not RH
alone.

## Dependency graph

```text
kernel decay and positivity
  -> A_(2j)(y) positive/analytic and differentiation is legal
  -> exact normalized Taylor sections S_m and uniform convergence on
     [epsilon,1/2] x [-R,R]

strict raw-moment monotonicity + a finite partition P
  -> local cross-endpoint coefficients L_(2j,i), U_(2j,i)
  -> local lower polynomial P_hat_(m,i) < C_y/A_0 on each cell

mesh(P)->0 with m,R,epsilon fixed
  -> L_(2j,i),U_(2j,i) -> m_(2j)(y) uniformly
  -> piecewise P_hat_(m,i) -> S_m uniformly

C_y>0 on one compact rectangle
  -> positive compact margin
  -> some exact S_m is positive there
  -> sufficiently fine local partition lower polynomials are positive there

positive local lower polynomials on that rectangle
  -> C_y>0 there

the preceding condition for every epsilon>0 and R<infinity
  <-> global open-strip C_y>0
  <-> RH

including strict y=0 boundary
  <-> RH + simplicity
```

## Caveats preventing circular use

1. The reverse implication from `C_y>0` to positive finite sections uses a
   positive compact minimum.  It is valid only after fixing `epsilon>0` and
   `R<infinity`; no uniform margin as `epsilon->0` or `R->infinity` is supplied.
2. `mesh(P)->0` at a fixed `m` gives only `S_m`.  It says nothing about large-x
   positivity and cannot be interchanged with `m->infinity` without an explicit
   diagonal quantifier.
3. A sufficient and equivalent diagonal formulation is: for every
   `epsilon>0` and finite `R`, there exist a finite `m` and a sufficiently fine
   finite partition whose every local lower polynomial is positive for
   `|x|<=R`.  Merely producing a sequence with shrinking mesh, without the
   positivity and exhaustion quantifiers, is not equivalent to RH.
4. The theorem that every fixed positive-width cell retains a bounded
   all-orders cross-endpoint radius is a separate high-order asymptotic input.
   It does not follow from normalized-moment monotonicity or from fixed-order
   mesh convergence.  Refinement evades that fixed-cell theorem only because
   the cell width itself tends to zero.
5. The Arb certificate in this directory proves monotonicity only for
   `m_2,...,m_12`; it is irrelevant to the all-orders equivalence except as a
   finite-order sharpening.  Using it as an all-j premise would be circular and
   invalid.

