# Finite positivity certificates and a cross-endpoint obstruction

This repository contains a scientific paper and a reproducible Arb/FLINT
certificate study for a defect kernel associated with the Riemann Xi
function. The paper contains a finite positivity theorem and an analytic
obstruction to scaling its fixed cross-endpoint hierarchy.

## Result

Let

$$
\Xi(z)=\xi\!\left(\frac12+iz\right)
      =\int_{\mathbb R}\Phi(u)e^{izu}\,du
$$

and, for `0 <= y <= 1/2`, define

$$
C_y(x)=\iint_{\mathbb R^2}
(u+v)^2\operatorname{sinhc}(y(u+v))
\Phi(u)\Phi(v)\cos(x(u-v))\,du\,dv.
$$

The degree-10 endpoint-moment certificate proves

$$
C_y(x)>0
\qquad
\left(0\le y\le\frac12,\ |x|\le R_{10}\right),
$$

where

$$
7.0362433<R_{10}<7.0362434.
$$

The proof does not enumerate zeros. It combines exact endpoint formulas for
Riemann-kernel moments, strict raw-moment monotonicity, a global degree-10
minorant for cosine, and outward-rounded Arb evaluation.

The same paper proves that, for every fixed `0 <= epsilon < 1/2`, the initial
positivity radii of the specified cross-endpoint polynomials satisfy

```text
sup_m Rhat_m^(epsilon) < infinity.
```

The second theorem is analytic and independent of the finite computations.
The polynomial sections converge locally uniformly to an exact mixed
trigonometric-hyperbolic transform that tends to minus infinity.

## Scope and classification

The finite band is a classification-C result. The bounded-radius theorem is a
classification-E result: it blocks the fixed cross-endpoint polynomial route,
not the Riemann Hypothesis, exact moment sections, or every adaptive partition
method. Neither theorem proves RH or improves the largest known finite height
through which researchers have verified RH.

## Files

- [`paper/main.pdf`](paper/main.pdf): compiled scientific paper.
- [`paper/main.tex`](paper/main.tex): LaTeX source.
- [`code/theta_moment_certificate.py`](code/theta_moment_certificate.py):
  load-bearing interval certificate.
- [`certificates/theta_moment_certificate.out`](certificates/theta_moment_certificate.out):
  captured audited output.
- [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md): exact reproduction steps and
  certificate scope.
- [`certificates/SHA256SUMS`](certificates/SHA256SUMS): release-artifact hashes.
- [`research/high_degree/radii.png`](research/high_degree/radii.png): graph of
  the certified finite radii; illustrative only, not the obstruction proof.
- [`research/README.md`](research/README.md): higher-degree records, analytic
  proof supplements, independent implementations, and audit registry.

## Quick verification

Install the pinned dependency and run:

```bash
uv run --with python-flint==0.9.0 python code/theta_moment_certificate.py
```

The final line must read:

```text
ALL CERTIFICATE ASSERTIONS PASSED
```

Do not run Python with `-O`; assertions form part of the certificate.

## Higher-degree verification

The supporting investigation in [`research/`](research/) contains all 175
certified higher-degree cases through degree 202, 816 endpoint moments,
independent clean-room and adversarial implementations, partition results,
minorant experiments, retained failures, the graph, and exact reproduction
commands. The authoritative paper now integrates both the finite theorem and
the analytic cross-endpoint obstruction.

## Licensing

- Software and certification scripts: GNU AGPL v3.0 only. See
  [`LICENSE`](LICENSE).
- Papers, manuscripts, LaTeX sources, figures, tables, and supplementary
  scholarly materials: Copyright (c) 2026 Leonard van Hemert. All rights
  reserved. See [`NOTICE`](NOTICE) for the full terms and scope.

Copyright (c) 2026 Leonard van Hemert.

## Citation

Use [`CITATION.cff`](CITATION.cff) and cite the exact Git commit used for any
reproduction or derivative analysis.
