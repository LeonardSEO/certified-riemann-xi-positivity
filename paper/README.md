# Paper build

`main.tex` is the source of the combined scientific article proving the
degree-10 finite positivity band and the fixed cross-endpoint bounded-radius
obstruction. `main.pdf` is the compiled release artifact.

The article includes `../research/high_degree/radii.png`. Build from this
repository layout so that the relative figure path resolves.

The paper, LaTeX source, figures, tables, and supplementary scholarly material
are Copyright (c) 2026 Leonard van Hemert. All rights reserved. See
`../NOTICE` for the full terms and scope.

Build with TeX Live:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```
