from embci_report.core import coverage_percent, render_markdown, summarize, threshold_failures


def sample_report():
    return {
        "suite": "motor-control",
        "tests": [
            {"name": "startup", "status": "passed", "duration_s": 0.1},
            {"name": "timeout", "status": "failed", "duration_s": 0.2, "message": "expected PASS"},
            {"name": "diag", "status": "skipped", "duration_s": 0},
        ],
        "coverage": {
            "statement": {"covered": 81, "total": 100},
            "function": {"covered": 9, "total": 10},
        },
    }


def test_summary_counts():
    summary = summarize(sample_report())
    assert summary.total == 3
    assert summary.failed == 1
    assert summary.duration_s == 0.3


def test_markdown_contains_failure():
    output = render_markdown(sample_report())
    assert "timeout — failed" in output
    assert "81.00%" in output


def test_threshold_failures():
    assert threshold_failures(sample_report(), {"statement": 85}) == ["statement: 81.00% < 85.00%"]


def test_empty_total_is_full_coverage():
    assert coverage_percent(0, 0) == 100.0
