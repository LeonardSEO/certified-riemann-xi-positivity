# Integrated v2 paper design

## Purpose

Replace `paper/main.tex` with one authoritative article that proves both the
certified degree-10 finite positivity band and the unconditional obstruction
to divergent radii in the fixed cross-endpoint hierarchy. The article must
not claim a proof of the Riemann Hypothesis, a new finite-height record, or an
obstruction to moment methods beyond the hierarchy actually analyzed.

The previous classification-C article remains permanently recoverable from
Git history, in particular commit `f2b5a1a`.

## Title and positioning

The title is:

> Finite Positivity Certificates and a Cross-Endpoint Obstruction for a
> Riemann Xi-Defect Kernel

The abstract states two results:

1. a zero-enumeration-free, Arb-certified degree-10 finite positivity band;
2. for every fixed `0 <= epsilon < 1/2`, boundedness of the initial positivity
   radii of the specified cross-endpoint polynomial hierarchy.

The abstract and conclusion explicitly state that neither result proves RH.
The analytic boundedness theorem, rather than the 175 computed cases, is the
principal new result of the combined article.

## Mathematical content

The article uses the existing normalizations for `xi`, `Xi`, the Riemann theta
kernel `Phi`, the defect kernel `C_y`, the weights `W_y`, and the raw moments
`A_(2j)(y)`. No normalization may be changed without rederiving every endpoint
identity and regenerating all certificates.

The article contains complete proofs of:

- the defect identity;
- the endpoint derivative formulas for the raw moments;
- strict raw-moment monotonicity;
- the strict global Taylor minorant for cosine;
- the degree-10 uniform lower polynomial and its finite-band consequence;
- the general cross-endpoint polynomial hierarchy;
- absolute and locally uniform convergence of the moment transforms;
- the exact mixed-limit formula, including the constant correction
  `1 - A_0(epsilon)/A_0(1/2)`;
- divergence of the relevant hyperbolic transform on the real axis;
- boundedness of `sup_m Rhat_m^(epsilon)` for every fixed
  `0 <= epsilon < 1/2`;
- failure of that coercive proof at `epsilon=1/2`;
- the distinction between fixed positive-width partitions and an all-orders
  diagonal refinement that reaches the RH-equivalent exact positivity
  condition.

The proof of boundedness may not depend on finite computation, a zero list,
RH, simplicity of zeta zeros, or a high-moment saddle heuristic.

## Article structure

1. Introduction and exact statement of the two main theorems.
2. Defect kernel and Hermite-Biehler implication.
3. Endpoint moments and strict raw-moment monotonicity.
4. Degree-10 lower polynomial and certified finite band.
5. General cross-endpoint hierarchy.
6. Entire moment transforms and exact mixed limit.
7. Fixed endpoint mismatch obstruction.
8. Endpoint, partition, and RH-equivalence boundary.
9. Higher-degree certified computation through degree 202.
10. Dependency graph, reproducibility, limitations, and conclusion.

The current generic positive-kernel counterexample remains only if it directly
clarifies why positivity and rapid decay alone do not imply global defect
positivity. It must not interrupt the main obstruction argument.

## Computational evidence

The article reports the certified study

```text
m = 0,...,20,25,30,40,50
epsilon = 0, 1/4, 1/8, 1/16, 1/32, 1e-2, 1e-3,
```

covering 175 cases and 816 endpoint moments through `A_202`. It states the
precision, root-bracketing method, derivative order, monotonicity certificate,
retained insufficient-precision failure, and independent 900-digit
cross-check.

`research/high_degree/radii.png` is included as an illustrative figure. Its
caption states that the figure is not evidence for the all-orders theorem and
that the analytic mixed-limit argument proves boundedness independently.

The complete machine-readable outputs remain repository supplements instead
of being copied into the article.

## Audit and dependency discipline

The article includes an explicit dependency graph separating:

- standard external facts about the Jacobi theta function, zeta functional
  equation, Fourier transforms, and Arb ball arithmetic;
- newly proved analytic lemmas;
- interval-certified finite statements;
- numerical illustrations;
- the final boundedness theorem;
- the exact unresolved RH-level positivity boundary.

The five reconstruction records and adversarial checks are summarized without
being described as external peer review. Every theorem used in the main
deduction must be present in the article or stated with checkable hypotheses.

## Repository changes

- Replace `paper/main.tex` with the integrated article.
- Rebuild and replace `paper/main.pdf`.
- Update `paper/README.md` to describe the combined result.
- Update the repository `README.md` so classification C and E are presented as
  results of the same authoritative paper.
- Update `CITATION.cff` title and abstract without changing the mixed-license
  policy.
- Update `certificates/SHA256SUMS` with the rebuilt PDF hash.
- Extend the existing paper CI only if required to verify the included figure
  or newly referenced artifacts.

The code and certification scripts remain AGPL-3.0-only. Papers, LaTeX
sources, figures, tables, and supplementary scholarly materials remain
Copyright (c) 2026 Leonard van Hemert, all rights reserved, under `NOTICE`.

## Acceptance criteria

- `paper/main.tex` compiles with the documented TeX Live toolchain.
- Every cross-reference and bibliography entry resolves.
- The PDF contains both principal theorems and the explicit non-RH disclaimer.
- The exact mixed-limit formula contains the constant correction and correct
  signs of both imaginary-axis transforms.
- The proof treats `epsilon=0`, `0<epsilon<1/2`, and `epsilon=1/2` separately.
- The higher-degree graph is legible and its caption is non-inferential.
- Text extraction finds no stale title, no CC BY-SA reference, and no RH-proof
  claim.
- Every rendered PDF page is visually inspected for clipping, overlap,
  malformed formulas, and bibliography defects.
- The original Arb certificate, clean-room reconstruction, 175-case verifier,
  adversarial tests, global-minorant certificate, partition certificate, and
  all published hashes pass.
- The final Git worktree is clean and the GitHub Actions workflow is green
  before any release is proposed.

## Excluded scope

- No Git tag, GitHub Release, Zenodo deposit, DOI, or arXiv submission.
- No claim that every endpoint-moment or partition method is blocked.
- No unproved uniform saddle-point asymptotic.
- No attempt to turn finite-height exclusion into a novelty claim.
- No change to repository licensing.
