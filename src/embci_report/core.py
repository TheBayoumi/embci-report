from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Any

VALID_STATUSES = {"passed", "failed", "skipped", "error"}


class ReportValidationError(ValueError):
    """Raised when an input report does not match the supported schema."""


@dataclass(frozen=True)
class Summary:
    suite: str
    total: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration_s: float


def _as_non_negative_int(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ReportValidationError(f"{field} must be a non-negative integer")
    return value


def validate_report(report: dict[str, Any]) -> None:
    if not isinstance(report, dict):
        raise ReportValidationError("report must be a JSON object")
    if not isinstance(report.get("suite"), str) or not report["suite"].strip():
        raise ReportValidationError("suite must be a non-empty string")
    tests = report.get("tests")
    if not isinstance(tests, list):
        raise ReportValidationError("tests must be a list")
    for index, test in enumerate(tests):
        if not isinstance(test, dict):
            raise ReportValidationError(f"tests[{index}] must be an object")
        if not isinstance(test.get("name"), str) or not test["name"].strip():
            raise ReportValidationError(f"tests[{index}].name must be a non-empty string")
        status = test.get("status")
        if status not in VALID_STATUSES:
            raise ReportValidationError(
                f"tests[{index}].status must be one of {sorted(VALID_STATUSES)}"
            )
        duration = test.get("duration_s", 0)
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration < 0:
            raise ReportValidationError(f"tests[{index}].duration_s must be non-negative")

    coverage = report.get("coverage", {})
    if not isinstance(coverage, dict):
        raise ReportValidationError("coverage must be an object")
    for metric, values in coverage.items():
        if not isinstance(metric, str) or not isinstance(values, dict):
            raise ReportValidationError("coverage metrics must map names to objects")
        covered = _as_non_negative_int(values.get("covered"), f"coverage.{metric}.covered")
        total = _as_non_negative_int(values.get("total"), f"coverage.{metric}.total")
        if covered > total:
            raise ReportValidationError(f"coverage.{metric}.covered cannot exceed total")


def summarize(report: dict[str, Any]) -> Summary:
    validate_report(report)
    statuses = [test["status"] for test in report["tests"]]
    return Summary(
        suite=report["suite"].strip(),
        total=len(statuses),
        passed=statuses.count("passed"),
        failed=statuses.count("failed"),
        skipped=statuses.count("skipped"),
        errors=statuses.count("error"),
        duration_s=round(sum(float(test.get("duration_s", 0)) for test in report["tests"]), 3),
    )


def coverage_percent(covered: int, total: int) -> float:
    return 100.0 if total == 0 else round((covered / total) * 100, 2)


def threshold_failures(report: dict[str, Any], thresholds: dict[str, float]) -> list[str]:
    validate_report(report)
    failures: list[str] = []
    coverage = report.get("coverage", {})
    for metric, minimum in thresholds.items():
        if metric not in coverage:
            failures.append(f"{metric}: missing (required {minimum:.2f}%)")
            continue
        values = coverage[metric]
        actual = coverage_percent(values["covered"], values["total"])
        if actual < minimum:
            failures.append(f"{metric}: {actual:.2f}% < {minimum:.2f}%")
    return failures


def render_markdown(report: dict[str, Any]) -> str:
    summary = summarize(report)
    lines = [
        f"# Embedded CI Report — {summary.suite}",
        "",
        "## Test summary",
        "",
        "| Total | Passed | Failed | Errors | Skipped | Duration |",
        "|---:|---:|---:|---:|---:|---:|",
        (
            f"| {summary.total} | {summary.passed} | {summary.failed} | "
            f"{summary.errors} | {summary.skipped} | {summary.duration_s:.3f}s |"
        ),
    ]

    failures = [t for t in report["tests"] if t["status"] in {"failed", "error"}]
    lines.extend(["", "## Failures", ""])
    if not failures:
        lines.append("No failed or errored tests.")
    else:
        for test in failures:
            lines.append(f"### {test['name']} — {test['status']}")
            lines.append("")
            lines.append(test.get("message") or "No diagnostic message supplied.")
            lines.append("")

    lines.extend(["## Coverage", ""])
    coverage = report.get("coverage", {})
    if not coverage:
        lines.append("No coverage data supplied.")
    else:
        lines.extend(["| Metric | Covered | Total | Percentage |", "|---|---:|---:|---:|"])
        for metric, values in sorted(coverage.items()):
            pct = coverage_percent(values["covered"], values["total"])
            lines.append(f"| {metric} | {values['covered']} | {values['total']} | {pct:.2f}% |")
    lines.append("")
    return "\n".join(lines)


def render_html(report: dict[str, Any]) -> str:
    summary = summarize(report)
    failures = [t for t in report["tests"] if t["status"] in {"failed", "error"}]
    failure_html = "<p>No failed or errored tests.</p>"
    if failures:
        failure_html = "".join(
            f"<section><h3>{escape(t['name'])} — {escape(t['status'])}</h3>"
            f"<pre>{escape(t.get('message') or 'No diagnostic message supplied.')}</pre></section>"
            for t in failures
        )

    coverage_rows = "".join(
        f"<tr><td>{escape(metric)}</td><td>{values['covered']}</td><td>{values['total']}</td>"
        f"<td>{coverage_percent(values['covered'], values['total']):.2f}%</td></tr>"
        for metric, values in sorted(report.get("coverage", {}).items())
    ) or "<tr><td colspan='4'>No coverage data supplied.</td></tr>"

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Embedded CI Report — {escape(summary.suite)}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:40px auto;padding:0 20px;line-height:1.5}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #bbb;padding:8px;text-align:left}}pre{{white-space:pre-wrap;background:#f5f5f5;padding:12px}}</style></head>
<body><h1>Embedded CI Report — {escape(summary.suite)}</h1>
<h2>Test summary</h2><table><tr><th>Total</th><th>Passed</th><th>Failed</th><th>Errors</th><th>Skipped</th><th>Duration</th></tr>
<tr><td>{summary.total}</td><td>{summary.passed}</td><td>{summary.failed}</td><td>{summary.errors}</td><td>{summary.skipped}</td><td>{summary.duration_s:.3f}s</td></tr></table>
<h2>Failures</h2>{failure_html}
<h2>Coverage</h2><table><tr><th>Metric</th><th>Covered</th><th>Total</th><th>Percentage</th></tr>{coverage_rows}</table>
</body></html>"""
