# Certified Riemann Xi Paper and Repository Design

## Purpose

Publish a public, reproducible research repository for the certified degree-10 finite positivity theorem for the Riemann Xi defect kernel. The repository must describe the result as a finite, classification-C theorem and must not present it as a proof of the Riemann Hypothesis.

## Repository

- GitHub owner: `LeonardSEO`
- Repository: `certified-riemann-xi-positivity`
- Visibility: public
- Default branch: `main`
- Repository description: `Certified finite positivity bands for a Riemann Xi defect kernel via endpoint moment bounds.`

## Research artifacts

The repository contains:

- a scientific LaTeX paper and compiled PDF;
- the load-bearing Arb/FLINT certificate;
- pinned Python dependency information;
- captured certificate output and SHA-256 checksums;
- reproducibility and claim-scope documentation;
- a GitHub Actions workflow that reruns the certificate;
- citation metadata.

The paper states the exact radius bracket

\[
7.0362433<R_{10}<7.0362434
\]

and proves

\[
C_y(x)>0\qquad
\left(0\le y\le\frac12,\ |x|\le R_{10}\right).
\]

It distinguishes this finite theorem from global positivity and from RH. It identifies the unresolved all-orders cross-endpoint radius condition without claiming that condition follows from RH.

## Licensing

- Software and repository automation: GNU Affero General Public License v3.0 only (`AGPL-3.0-only`).
- Paper text, LaTeX source, and figures: Creative Commons Attribution-ShareAlike 4.0 International (`CC-BY-SA-4.0`).
- `NOTICE` assigns copyright to Leonard van Hemert and maps files to the applicable license.
- No proprietary, noncommercial, no-fork, or confidentiality restriction is added. Such restrictions would conflict with the approved open-source design.

## Verification

The release is acceptable only when:

1. the pinned certificate exits with status zero and prints `ALL CERTIFICATE ASSERTIONS PASSED`;
2. the LaTeX compile skill produces `paper/main.pdf`;
3. the PDF renders without missing pages or obvious layout defects;
4. checksums match the committed artifacts;
5. the repository contains no RH-proof claim, local absolute path, secret, or temporary research file;
6. the public GitHub repository exposes the expected files on `main`.

## Publication posture

The title is `Certified Finite Positivity Bands for a Riemann Xi-Defect Kernel via Endpoint Moment Bounds`. The abstract and conclusion call the result a zero-enumeration-free finite certificate. The paper notes that existing verified-zero computations reach much greater height, so the finite-height corollary is not a record.
