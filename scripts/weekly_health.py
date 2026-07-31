from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    report_path = Path("examples/report.json")
    data = json.loads(report_path.read_text(encoding="utf-8"))
    failed = [test for test in data["tests"] if test["status"] in {"failed", "error"}]
    print("# Weekly product-health report")
    print()
    print(f"Example report tests: {len(data['tests'])}")
    print(f"Example failures: {len(failed)}")
    if failed:
        print("ATTENTION_REQUIRED")
        print("The bundled example contains failed or errored tests and should be reviewed.")
    else:
        print("No attention required.")


if __name__ == "__main__":
    main()
