# embci-report

[![CI](https://github.com/TheBayoumi/embci-report/actions/workflows/ci.yml/badge.svg)](https://github.com/TheBayoumi/embci-report/actions/workflows/ci.yml)

A small, vendor-neutral CLI that converts embedded-software test and coverage JSON into readable Markdown or HTML reports.

[View the five-minute demo](docs/demo.md) · [See the verified generated report](examples/generated-report.md) · [Request a paid integration](https://github.com/TheBayoumi/embci-report/issues/new?template=paid_integration_request.yml)

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

## Need an integration now?

Paid fixed-scope services are available without waiting for GitHub Sponsors approval:

- $49 integration assessment
- generic adapters from $149
- CI integration packs from $299

[Open the paid integration request](https://github.com/TheBayoumi/embci-report/issues/new?template=paid_integration_request.yml) using only public, fictional, or sanitized information. After the request is accepted, the fixed $49 assessment can be paid through [PayPal](https://paypal.me/TheBayoumi/49USD). Adapter and CI integration payments are requested only after written scope and pricing are agreed.

See [SERVICES.md](SERVICES.md) for deliverables, payment terms, and boundaries.

## Support development

The public CLI remains useful without payment. A GitHub Sponsors application has been submitted, but the Sponsors listing and paid tiers are not public yet.

Planned sponsor benefits include:

- reusable GitHub Actions and GitLab CI templates
- generic JUnit XML and CSV adapters
- early access to new vendor-neutral integrations
- priority triage for bounded compatibility requests

The private sponsor kit has already been implemented and transferred to the organization-owned private repository `TheBayoumi-Labs/embci-report-sponsor-kit`. After GitHub approves the Sponsors profile, that repository will be attached to the appropriate sponsorship tiers for automatic access management.

One-time support is available through [PayPal.Me](https://paypal.me/TheBayoumi).

See [SUPPORT.md](SUPPORT.md) for the planned tiers and boundaries.

## Safety and confidentiality

Do not upload employer-owned test data, proprietary report formats, confidential source code, customer information, or restricted tool exports. Reproduction cases must be fictional, sanitized, or independently created.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Integration requests can be submitted through the repository issue template using sanitized examples only.

## License

MIT
