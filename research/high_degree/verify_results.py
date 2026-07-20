#!/usr/bin/env python3
"""Structural verification for committed high-degree JSONL result files."""
from __future__ import annotations
import json
import sys
from fractions import Fraction
from pathlib import Path

EPS = ("0", "1/4", "1/8", "1/16", "1/32", "1e-2", "1e-3")
MS = tuple(range(21)) + (25, 30, 40, 50)

def records(path: Path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def interval(case):
    c=case["certified"]; den=1 << c["t_dyadic_exponent"]
    return (Fraction(int(c["t_lower_dyadic_numerator"]),den),
            Fraction(int(c["t_upper_dyadic_numerator"]),den))

def main(root: Path) -> None:
    full=records(root/"full_dps700.jsonl")
    cases={(r["epsilon"],r["m"]):r for r in full if r["record"]=="case"}
    assert set(cases)==set((e,m) for e in EPS for m in MS)
    assert all(r["failure"] is None for r in cases.values())
    assert all(r["certified"]["certified_first_root"] for r in cases.values())
    assert all(r["certified"]["certified_strictly_decreasing_before_root"] for r in cases.values())
    batches=[r for r in full if r["record"]=="moment_batch"]
    assert len(batches)==8 and all(len(r["moments"])==102 for r in batches)
    cross=records(root/"crosscheck_m50_dps900.jsonl")
    cc={(r["epsilon"],r["m"]):r for r in cross if r["record"]=="case"}
    for e in EPS:
        lo,hi=interval(cases[(e,50)]); lo2,hi2=interval(cc[(e,50)])
        assert lo <= lo2 < hi2 <= hi
    tail=records(root/"tail_dps900_bits240.jsonl")
    tc={(r["epsilon"],r["m"]):r for r in tail if r["record"]=="case"}
    for e in EPS:
        seq=[tc[(e,m)] for m in (19,20,25,30)]
        assert all(interval(a)[1] < interval(b)[0] for a,b in zip(seq,seq[1:]))
    print("PASS: 175 certified cases, 816 endpoint moments, dps900 containment, tail increases through m=30")

if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent))
