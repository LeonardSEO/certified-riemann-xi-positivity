# Paper build

`main.tex` is the source of the scientific article. `main.pdf` is the compiled
release artifact.

The paper material is licensed under CC BY-SA 4.0. See
`../LICENSES/CC-BY-SA-4.0.txt`.

Build with TeX Live:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```
