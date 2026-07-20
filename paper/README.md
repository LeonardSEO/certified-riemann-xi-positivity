# Paper build

`main.tex` is the source of the scientific article. `main.pdf` is the compiled
release artifact.

The paper, LaTeX source, figures, tables, and supplementary scholarly material
are Copyright (c) 2026 Leonard van Hemert. All rights reserved. See
`../NOTICE` for the full terms and scope.

Build with TeX Live:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```
