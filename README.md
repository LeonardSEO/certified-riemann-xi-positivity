# Certified finite positivity bands for a Riemann Xi-defect kernel

This repository contains a scientific paper and a reproducible Arb/FLINT
certificate for a finite positivity theorem associated with the Riemann Xi
function.

## Result

Let

\[
\Xi(z)=\xi\!\left(\frac12+iz\right)
      =\int_{\mathbb R}\Phi(u)e^{izu}\,du
\]

and, for `0 <= y <= 1/2`, define

\[
C_y(x)=\iint_{\mathbb R^2}
(u+v)^2\operatorname{sinhc}(y(u+v))
\Phi(u)\Phi(v)\cos(x(u-v))\,du\,dv.
\]

The degree-10 endpoint-moment certificate proves

\[
C_y(x)>0
\qquad
\left(0\le y\le\frac12,\ |x|\le R_{10}\right),
\]

where

\[
7.0362433<R_{10}<7.0362434.
\]

The proof does not enumerate zeros. It combines exact endpoint formulas for
Riemann-kernel moments, strict raw-moment monotonicity, a global degree-10
minorant for cosine, and outward-rounded Arb evaluation.

## Scope

This is a finite, classification-C theorem. It does not prove the Riemann
Hypothesis and does not improve the largest known finite height through which
researchers have verified RH. The open problem for this method is an
all-orders estimate that forces the positivity radii of the cross-endpoint
minorants to grow without bound.

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

## Higher-degree investigation

The follow-up investigation is in [`research/`](research/). Its principal
classification is **E — cross-endpoint route blocked**: for every fixed
`0 <= epsilon < 1/2`, the stated cross-endpoint radii have a finite supremum.
The proof, all 175 certified higher-degree cases through degree 202, the
independent clean-room and adversarial implementations, partition results,
minorant experiments, graph, failures, and reproduction commands are indexed
in [`research/README.md`](research/README.md). The paper itself is unchanged.

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
