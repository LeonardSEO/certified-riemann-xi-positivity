# Independent higher-degree adversarial audit

This directory is a second implementation of the moment/root calculation. It
uses only the definitions of `H_(2j)`, the endpoint identities, and
`Phat_m^(epsilon)` from the paper. It does not import or call the published
certificate in `code/`.

[`ANALYTIC_OBSTRUCTION.md`](ANALYTIC_OBSTRUCTION.md) gives the independent
all-orders verdict: the mixed cross-endpoint radii have a finite supremum for
every fixed `0 <= epsilon < 1/2`.

All load-bearing arithmetic uses `python-flint` Arb/Acb balls. The harness:

- derives endpoint moments by an explicit double Leibniz sum;
- cross-checks derivative indexing with a separately constructed formal-series
  `H_(2j)`;
- rejects a formal-series cap that cannot contain the highest derivative;
- compares the minimal cap with an overprovisioned cap;
- checks endpoint normalization inequalities;
- isolates every complex root of `Q(t)=Phat(sqrt(t))` and `Q'(t)` with Acb;
- brackets the initial positive root by rational-point Arb sign tests;
- probes cancellation as `epsilon` tends to zero; and
- evaluates at `x=1e100` by Arb Horner arithmetic to avoid machine overflow.

## Reproduce

Run the tests:

```bash
cd research/adversarial
uv run --with python-flint==0.9.0 python -m unittest -v test_adversarial.py
```

Run the full finite scan used in `RESULTS.md`:

```bash
cd research/adversarial
uv run --with python-flint==0.9.0 python higher_degree_audit.py \
  --max-m 12 --precision 384
```

Probe a chosen epsilon independently:

```bash
uv run --with python-flint==0.9.0 python higher_degree_audit.py \
  --max-m 8 --precision 512 --epsilon 1/1000000
```

The scan is a finite audit, not evidence for an all-orders limit. Acb root
isolation certifies the reported finite-degree root counts; it does not turn a
finite table into a proof about `sup_m`.
