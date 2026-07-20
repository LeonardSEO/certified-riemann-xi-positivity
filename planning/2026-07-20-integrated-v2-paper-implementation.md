# Integrated v2 Paper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the finite-band-only paper with one authoritative article proving the degree-10 finite band and the fixed cross-endpoint bounded-radius obstruction.

**Architecture:** Preserve the audited definitions and finite certificate proof, then insert the general hierarchy, entire-transform limit, and unconditional obstruction as a second theorem chain. Keep machine-readable computation in `research/`, include one generated graph, and synchronize all public metadata with the combined paper.

**Tech Stack:** LaTeX/latexmk, Python 3.12, python-flint 0.9.0, Arb/FLINT ball arithmetic, GitHub Actions, pypdf/PyMuPDF for PDF inspection.

## Global Constraints

- Do not change the normalization of `xi`, `Xi`, `Phi`, `W_y`, `C_y`, or `A_(2j)(y)`.
- Do not claim RH, a new finite-height record, or an obstruction beyond the fixed cross-endpoint hierarchy.
- Keep software AGPL-3.0-only and scholarly materials all rights reserved under `NOTICE`.
- Preserve the previous article through Git history at commit `f2b5a1a`.
- Do not create a tag, release, Zenodo deposit, DOI, or arXiv submission.

---

### Task 1: Establish a verified baseline

**Files:**
- Read: `paper/main.tex`
- Read: `research/README.md`
- Read: `research/adversarial/ANALYTIC_OBSTRUCTION.md`
- Read: `research/minorants/mixed_limit_theorem.md`

**Interfaces:**
- Consumes: Existing theorem labels, endpoint identities, certified outputs, and obstruction audit.
- Produces: A baseline record showing the current certificate and research verifiers pass before editing.

- [ ] **Step 1: Verify repository and branch state**

  Run `git status --short --branch` and confirm the only unpublished commit is the approved planning material.

- [ ] **Step 2: Run the finite certificate**

  Run:

  ```bash
  uv run --with python-flint==0.9.0 python code/theta_moment_certificate.py
  ```

  Expected terminal marker: `ALL CERTIFICATE ASSERTIONS PASSED`.

- [ ] **Step 3: Run the higher-degree verifier and adversarial tests**

  Run:

  ```bash
  uv run --with python-flint==0.9.0 python research/high_degree/verify_results.py
  PYTHONPATH=research/adversarial uv run --with python-flint==0.9.0 \
    python -m unittest -v research/adversarial/test_adversarial.py
  ```

  Expected: 175 certified cases pass and seven adversarial tests report `OK`.

### Task 2: Replace the article with the integrated proof

**Files:**
- Modify: `paper/main.tex`

**Interfaces:**
- Consumes: Exact formulas and proof obligations from Task 1 source files.
- Produces: The two main theorem labels `thm:finite-band` and `thm:obstruction`, plus a complete dependency chain.

- [ ] **Step 1: Update title, abstract, and theorem summary**

  Use the title `Finite Positivity Certificates and a Cross-Endpoint Obstruction for a Riemann Xi-Defect Kernel`. State both results and the non-RH scope in the abstract and introduction.

- [ ] **Step 2: Preserve and relabel the finite-band proof**

  Retain the defect identity, endpoint moment identities, raw-moment monotonicity, cosine minorant, degree-10 lower polynomial, Arb enclosure, boundary strictness, and finite zero consequence without changing their formulas.

- [ ] **Step 3: Add the arbitrary-degree hierarchy**

  Define `Q_m^(epsilon)` with degree `4m+2`, positive even-index endpoint coefficients, negative odd-index endpoint coefficients, and constant term one.

- [ ] **Step 4: Prove entire convergence and the mixed-limit formula**

  Define `G_y(x)=C_y(ix)` and prove locally uniform convergence from the theta-kernel decay. State exactly

  ```text
  F_epsilon(x)
   = 1-a/b
     +(G_epsilon(x)+C_epsilon(x))/(2b)
     -(G_(1/2)(x)-C_(1/2)(x))/(2a),
  ```

  where `a=A_0(epsilon)` and `b=A_0(1/2)`.

- [ ] **Step 5: Prove the bounded-radius theorem**

  Establish `0<a<b`, `G_(1/2)>=G_epsilon`, `|C_y|<=A_0(y)`, and `G_epsilon(x)>=c cosh(delta x)`. Deduce `F_epsilon(x)->-infinity`, pass to sufficiently large finite sections by local uniform convergence, and handle the finitely many remaining polynomials using their negative leading coefficients.

- [ ] **Step 6: Delimit endpoints and partitions**

  Treat `epsilon=0`, `0<epsilon<1/2`, and `epsilon=1/2` separately. Explain why fixed positive-width partition cells inherit the obstruction while a fully refined diagonal scheme reaches the RH-equivalent positivity boundary.

- [ ] **Step 7: Add computation, dependency graph, and limitations**

  Include `research/high_degree/radii.png`, report the exact certified domain and retained failure, and label the graph illustrative. Add a dependency list separating analytic proofs, interval certificates, numerical illustrations, and unresolved RH-equivalent positivity.

### Task 3: Synchronize repository metadata

**Files:**
- Modify: `README.md`
- Modify: `paper/README.md`
- Modify: `CITATION.cff`

**Interfaces:**
- Consumes: Final title, abstract, theorem statements, and scope from Task 2.
- Produces: Consistent public descriptions and citation metadata.

- [ ] **Step 1: Update the repository README**

  Present the finite-band and obstruction theorems as the two results of the authoritative paper. Link the graph, proof supplements, code, and PDF. Remove the statement that the paper is unchanged.

- [ ] **Step 2: Update the paper build README**

  Describe the included graph path and combined article while preserving the build command and all-rights-reserved notice.

- [ ] **Step 3: Update citation metadata**

  Change the title and abstract in `CITATION.cff`; retain author, repository URL, release date, rights message, and keywords, adding cross-endpoint obstruction as a keyword.

### Task 4: Build and inspect the scientific PDF

**Files:**
- Modify: `paper/main.pdf`
- Modify: `certificates/SHA256SUMS`

**Interfaces:**
- Consumes: Final `paper/main.tex` and `research/high_degree/radii.png`.
- Produces: Compiled, visually reviewed PDF and matching SHA-256 entry.

- [ ] **Step 1: Compile with the documented toolchain**

  Run the bundled LaTeX compile helper. If local TeX is unavailable, push only the source commit, let the existing GitHub paper job compile it, and download that exact workflow artifact.

- [ ] **Step 2: Check extracted content**

  Use pypdf to assert presence of both theorem conclusions, the constant correction, the non-RH disclaimer, `All rights reserved`, and `AGPL-3.0-only`; assert absence of `CC BY-SA` and any stale title.

- [ ] **Step 3: Render and inspect every page**

  Render all pages with PyMuPDF into `tmp/pdfs/`, create a contact sheet, and inspect formulas, figure resolution, margins, page headers, references, and the final licensing paragraph.

- [ ] **Step 4: Record the PDF hash**

  Replace only the `paper/main.pdf` line in `certificates/SHA256SUMS` with the new SHA-256 digest and verify the complete checksum file.

### Task 5: Run the complete acceptance suite and publish the branch state

**Files:**
- Verify: `.github/workflows/verify.yml`
- Verify: `certificates/SHA256SUMS`
- Verify: `research/SHA256SUMS`
- Verify: `research/high_degree/SHA256SUMS`

**Interfaces:**
- Consumes: All artifacts from Tasks 1-4.
- Produces: A clean commit on `main`, synchronized public repository, and green GitHub Actions evidence.

- [ ] **Step 1: Run local acceptance checks**

  Run `git diff --check`, all checksum verifiers, the original certificate, clean-room reconstruction, 175-case verifier, seven adversarial tests, global-minorant reproduction, and 1000-cell partition certificate.

- [ ] **Step 2: Audit public wording**

  Search tracked text for stale title, CC licensing, RH-proof language, local absolute paths, and claims that the graph proves asymptotic boundedness. Correct every false or ambiguous match.

- [ ] **Step 3: Commit and push**

  Commit the integrated article and metadata with a Conventional Commit message, push `main`, and record the exact commit SHA.

- [ ] **Step 4: Verify GitHub Actions**

  Wait for the certificate, higher-degree research, and paper jobs. Completion requires all three jobs to conclude `success`; deprecation warnings from third-party action runtimes must be reported separately from mathematical verification.
