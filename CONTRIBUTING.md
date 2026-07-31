# Contributing

Contributions are welcome when they are vendor-neutral and can be reviewed without confidential material.

## Development

```bash
python -m pip install -e .
pytest
```

## Pull requests

- Keep changes focused.
- Add or update tests.
- Use fictional or independently created fixtures.
- Document schema or behavior changes.
- Do not commit generated caches, credentials, binaries, proprietary exports, or employer-owned data.

## Integration requests

Use the integration-request issue template and provide:

- the public format specification or documentation
- a fictional minimal input example
- the expected `embci-report` JSON output
- the intended CI environment

Requests depending on confidential files cannot be evaluated.
