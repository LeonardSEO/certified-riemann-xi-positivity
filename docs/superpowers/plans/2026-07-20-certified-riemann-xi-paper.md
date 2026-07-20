# Certified Riemann Xi Paper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify, and publish a public scientific-paper repository for the certified degree-10 Riemann Xi defect-kernel positivity theorem.

**Architecture:** Keep the mathematical paper, executable certificate, captured evidence, and repository metadata in separate directories. The Python certificate remains the sole load-bearing computation; the paper proves every analytic identity and explains the finite arithmetic certificate. GitHub Actions reruns the pinned certificate on every push.

**Tech Stack:** LaTeX, Python 3.12, python-flint 0.9.0, FLINT/Arb ball arithmetic, Git, GitHub Actions, GitHub CLI.

## Global Constraints

- State classification C and never claim a proof of RH.
- Publish the repository publicly under `LeonardSEO/certified-riemann-xi-positivity`.
- License software as `AGPL-3.0-only` and paper material as `CC-BY-SA-4.0`.
- Preserve the exact radius bracket `7.0362433 < R_10 < 7.0362434`.
- Keep the certificate reproducible with `python-flint==0.9.0` and ordinary Python execution without `-O`.
- Do not copy unrelated files from `sources/` or `tmp/`.

---

### Task 1: Repository skeleton and licensing

**Files:**
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `LICENSES/CC-BY-SA-4.0.txt`
- Create: `NOTICE`
- Create: `README.md`
- Create: `CITATION.cff`

**Interfaces:**
- Consumes: approved public dual-license design.
- Produces: repository-wide file layout and claim-scope contract.

- [ ] **Step 1: Create the directory structure**

```bash
mkdir -p paper code certificates LICENSES .github/workflows
```

- [ ] **Step 2: Add standard licenses and scope notice**

Use the unmodified AGPL-3.0-only legal text for software and the official CC-BY-SA-4.0 legal-code URI for paper material. Map paths in `NOTICE`.

- [ ] **Step 3: Add repository metadata**

Write `README.md` and `CITATION.cff` with the theorem, finite scope, reproduction command, author, and licenses.

- [ ] **Step 4: Validate claim scope**

```bash
rg -n "proof of (the )?Riemann Hypothesis|RH breakthrough|baanbrekend" README.md NOTICE CITATION.cff
```

Expected: no misleading positive claim; contextual negations may appear only in explicit limitations.

### Task 2: Reproducible certificate package

**Files:**
- Create: `code/theta_moment_certificate.py`
- Create: `code/requirements.txt`
- Create: `certificates/theta_moment_certificate.out`
- Create: `certificates/SHA256SUMS`
- Create: `.github/workflows/verify.yml`

**Interfaces:**
- Consumes: audited certificate from `tmp/theta_moment_certificate.py`.
- Produces: pinned executable and captured evidence used by the paper.

- [ ] **Step 1: Copy the audited certificate**

```bash
cp tmp/theta_moment_certificate.py code/theta_moment_certificate.py
```

- [ ] **Step 2: Pin the dependency**

```text
python-flint==0.9.0
```

- [ ] **Step 3: Run and capture the certificate**

```bash
uv run --with python-flint==0.9.0 python code/theta_moment_certificate.py | tee certificates/theta_moment_certificate.out
```

Expected: exit 0 and final line `ALL CERTIFICATE ASSERTIONS PASSED`.

- [ ] **Step 4: Generate checksums**

```bash
shasum -a 256 code/theta_moment_certificate.py certificates/theta_moment_certificate.out
```

- [ ] **Step 5: Add continuous verification**

The workflow installs `python-flint==0.9.0`, runs the certificate without Python optimization, and fails unless the success marker appears.

### Task 3: Scientific paper

**Files:**
- Create: `paper/main.tex`
- Create: `paper/README.md`
- Create: `paper/main.pdf`

**Interfaces:**
- Consumes: the proved analytic lemmas and certified values.
- Produces: peer-readable theorem, proof, limitations, novelty comparison, and reproducibility section.

- [ ] **Step 1: Write the LaTeX source**

Include definitions, the defect identity, endpoint moment formulas, strict raw-moment bounds, the global degree-10 cosine minorant, Arb certificate, finite zero consequence, counterexample, exact remaining gap, literature comparison, and license note.

- [ ] **Step 2: Compile with the required skill**

```bash
python3 /path/to/latex-plugin/scripts/compile_latex.py "$PWD/paper/main.tex" --output-directory "$PWD/paper/build" --json
```

Expected: successful compilation and a PDF copied to `paper/main.pdf`.

- [ ] **Step 3: Inspect the rendered PDF**

Render pages to images, check page count, fonts, equations, tables, references, and absence of clipping.

### Task 4: Repository verification and publication

**Files:**
- Verify: all repository files.
- Publish: `LeonardSEO/certified-riemann-xi-positivity` on branch `main`.

**Interfaces:**
- Consumes: verified paper and certificate tree.
- Produces: public GitHub repository URL and immutable commit SHA.

- [ ] **Step 1: Run full local verification**

```bash
uv run --with python-flint==0.9.0 python code/theta_moment_certificate.py
test -s paper/main.pdf
shasum -a 256 -c certificates/SHA256SUMS
rg -n "/Users/|T[B]D|T[O]DO" README.md paper code certificates NOTICE CITATION.cff
```

Expected: certificate passes, PDF is nonempty, checksums match, and no local paths or placeholders remain.

- [ ] **Step 2: Initialize and commit intentionally**

```bash
git init -b main
git add .gitignore .github CITATION.cff LICENSE LICENSES NOTICE README.md paper code certificates docs
git commit -m "publish certified Riemann Xi positivity paper"
```

- [ ] **Step 3: Create and push the public repository**

```bash
gh repo create LeonardSEO/certified-riemann-xi-positivity --public --source=. --remote=origin --push --description "Certified finite positivity bands for a Riemann Xi defect kernel via endpoint moment bounds."
```

- [ ] **Step 4: Verify the public result**

```bash
gh repo view LeonardSEO/certified-riemann-xi-positivity --json nameWithOwner,visibility,url,defaultBranchRef
git ls-remote --heads origin main
```

Expected: public repository, default branch `main`, and remote head equal to the local commit.
