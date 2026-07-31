# embci-report

A small, vendor-neutral CLI that converts embedded-software test and coverage JSON into readable Markdown or HTML reports.

## Why it exists

Embedded CI pipelines often produce dense logs that are difficult to review in pull requests. `embci-report` creates a compact summary, groups failed tests, reports coverage, and can enforce coverage thresholds through exit codes.

## Quick start

```bash
python -m pip install -e .
embci-report examples/report.json --format markdown --output report.md
embci-report examples/report.json --fail-under statement=80 --fail-under function=80
```

Exit codes:

- `0`: report generated and thresholds passed
- `1`: invalid input or file error
- `2`: one or more coverage thresholds failed

## Input schema

```json
{
  "suite": "unit-name",
  "tests": [
    {"name": "test-name", "status": "passed|failed|skipped|error", "duration_s": 0.12, "message": "optional"}
  ],
  "coverage": {
    "statement": {"covered": 80, "total": 100}
  }
}
```

## Monetization structure

The public repository should remain useful on its own. Sponsor-only material belongs in a separate private organization repository and may include:

- CI templates for common embedded workflows
- report-adapter examples for exported vendor-neutral JSON/XML
- management dashboards and trend reports
- priority compatibility requests

Do not upload employer-owned test data, proprietary report formats, or confidential source code.

## Roadmap

- JUnit XML adapter
- SARIF output for GitHub code scanning annotations
- historical trend charts
- generic CSV adapter
- sponsor-only pipeline templates

## License

MIT
