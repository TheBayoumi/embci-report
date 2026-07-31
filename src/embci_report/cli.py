from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import ReportValidationError, render_html, render_markdown, threshold_failures


def _threshold(value: str) -> tuple[str, float]:
    try:
        metric, raw = value.split("=", 1)
        minimum = float(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("threshold must be metric=percentage") from exc
    if not metric or minimum < 0 or minimum > 100:
        raise argparse.ArgumentTypeError("threshold percentage must be between 0 and 100")
    return metric, minimum


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="embci-report")
    parser.add_argument("input", type=Path, help="Path to the JSON report")
    parser.add_argument("--format", choices=("markdown", "html"), default="markdown")
    parser.add_argument("--output", type=Path, help="Write output to this file instead of stdout")
    parser.add_argument(
        "--fail-under",
        action="append",
        type=_threshold,
        default=[],
        metavar="METRIC=PERCENT",
        help="Fail with exit code 2 when coverage is below a threshold",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = json.loads(args.input.read_text(encoding="utf-8"))
        output = render_markdown(report) if args.format == "markdown" else render_html(report)
        thresholds = dict(args.fail_under)
        failures = threshold_failures(report, thresholds)
    except (OSError, json.JSONDecodeError, ReportValidationError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)

    if failures:
        print("coverage threshold failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
