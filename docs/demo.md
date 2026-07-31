# Five-minute demo

This demo uses only fictional embedded-controller data from [`examples/report.json`](../examples/report.json).

## 1. Install locally

```bash
python -m pip install -e .
```

## 2. Generate a pull-request-friendly report

```bash
embci-report examples/report.json --format markdown --output report.md
```

The verified output is committed as [`examples/generated-report.md`](../examples/generated-report.md). It summarizes test outcomes and statement, function, MCDC-condition, and MCDC-pair coverage in a reviewable format.

## 3. Enforce CI policy

```bash
embci-report examples/report.json \
  --fail-under statement=90 \
  --fail-under function=85 \
  --fail-under mcdc_condition=80 \
  --fail-under mcdc_pair=75
```

The command exits with:

- `0` when all configured thresholds pass
- `2` when one or more coverage thresholds fail
- `1` for invalid input or file errors

## Where it fits

A typical pipeline converts a vendor or test-framework export into the public `embci-report` JSON schema, then runs the CLI to produce Markdown or HTML evidence and enforce coverage policy.

```text
Test or coverage export
        ↓
Sanitized adapter
        ↓
embci-report JSON
        ↓
Markdown / HTML + CI exit code
```

## Need another input format?

Use the [paid integration request form](https://github.com/TheBayoumi/embci-report/issues/new?template=paid_integration_request.yml) for a documented, public, fictional, or sanitized format.

- Integration assessment: **$49**
- Generic adapter: **from $149**
- CI integration pack: **from $299**

Do not upload proprietary source code, employer-owned reports, credentials, customer data, or licensed vendor exports.
