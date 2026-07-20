#!/usr/bin/env python3
"""Plot certified root brackets from the JSONL result file.

The graph is a discovery aid only.  The plotted center is obtained by
converting each exact dyadic t=x^2 bracket to binary64 after certification.
The JSONL dyadic numerators and exponents, not the PNG, are the certificate.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("full_dps700.jsonl"))
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("radii.png"))
    args = parser.parse_args()

    rows = []
    with args.input.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("record") != "case":
                continue
            certified = record["certified"]
            denominator = 1 << certified["t_dyadic_exponent"]
            lower_t = int(certified["t_lower_dyadic_numerator"]) / denominator
            upper_t = int(certified["t_upper_dyadic_numerator"]) / denominator
            rows.append((record["epsilon"], record["m"], math.sqrt((lower_t + upper_t) / 2)))

    import matplotlib.pyplot as plt

    for epsilon in sorted({row[0] for row in rows}):
        points = sorted((m, radius) for label, m, radius in rows if label == epsilon)
        plt.plot([p[0] for p in points], [p[1] for p in points], marker="o", ms=3, label=epsilon)
    plt.xlabel("m (polynomial degree 4m+2)")
    plt.ylabel("certified first-root bracket center")
    plt.title("Cross-endpoint positivity radii (graph is not a certificate)")
    plt.grid(alpha=0.25)
    plt.legend(title="epsilon", ncol=2)
    plt.tight_layout()
    plt.savefig(args.output, dpi=180)


if __name__ == "__main__":
    main()
