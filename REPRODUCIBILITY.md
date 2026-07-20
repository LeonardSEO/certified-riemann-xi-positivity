# Reproducibility

## Certified computation

The load-bearing finite computation uses:

- Python 3.12;
- `python-flint==0.9.0`;
- FLINT 3.6.0 in the audited wheel;
- Arb midpoint-radius ball arithmetic at 269-bit precision;
- a formal-series cap of 18, with derivatives required only through order 12.

Run the certificate without Python's `-O` flag because the certificate uses
assertions as proof obligations:

```bash
uv run --with python-flint==0.9.0 python code/theta_moment_certificate.py
```

or:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r code/requirements.txt
python code/theta_moment_certificate.py
```

A successful run ends with:

```text
ALL CERTIFICATE ASSERTIONS PASSED
```

The committed output in `certificates/theta_moment_certificate.out` records one
audited run. `certificates/SHA256SUMS` identifies the exact code, output, and PDF
published in the repository.

## Paper

The repository commits the compiled PDF. To rebuild it with the Codex LaTeX
compiler wrapper used for the release:

```bash
python3 /path/to/latex-plugin/scripts/compile_latex.py paper/main.tex \
  --output-directory paper/build --json
```

The LaTeX source uses standard packages and also compiles with a normal TeX
Live installation:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=paper/build paper/main.tex
```

Copy `paper/build/main.pdf` to `paper/main.pdf` after a successful build.
The build must retain the repository layout because the article includes
`research/high_degree/radii.png` by relative path.

## What the certificate proves

The program encloses the twelve endpoint moments, five cross-endpoint ratios,
the Bernstein coefficients of the derivative polynomial on `0 <= t <= 51`,
the shifted power coefficients for `t >= 51`, and the two rational root-bracket
signs. The analytic identities connecting those quantities to the Riemann
theta kernel appear in the paper and are not delegated to the program.

## Higher-degree and obstruction study

The bounded-radius theorem in the paper is analytic and does not depend on
the computed radii. The supporting interval records cover 175 cases and 816
endpoint moments through `A_202`. Verify them and the independent adversarial
implementation with:

```bash
uv run --with python-flint==0.9.0 \
  python research/high_degree/verify_results.py
PYTHONPATH=research/adversarial uv run --with python-flint==0.9.0 \
  python -m unittest -v research/adversarial/test_adversarial.py
```

The clean-room reconstruction, global-minorant calculation, and partition
certificate have exact commands in `research/README.md`. Their committed
inputs and outputs are covered by `research/SHA256SUMS` and
`research/high_degree/SHA256SUMS`.
