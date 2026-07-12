from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "data" / "eval" / "golden.jsonl"


def check_golden(input_path: Path) -> int:
    errors: list[str] = []
    records: list[dict] = []
    seen_ids: set[object] = set()

    try:
        lines = input_path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        print(f"Error: could not read {input_path}: {error}", file=sys.stderr)
        return 1

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"Line {line_number}: invalid JSON ({error.msg})")
            continue

        if not isinstance(record, dict):
            errors.append(f"Line {line_number}: expected a JSON object")
            continue

        records.append(record)
        record_id = record.get("id")
        if record_id in seen_ids:
            errors.append(f"Line {line_number}: duplicate id {record_id!r}")
        else:
            seen_ids.add(record_id)

        for field in ("question", "expected"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"Line {line_number}: {field} must be a non-empty string")

    categories = Counter(str(record.get("category", "<missing>")) for record in records)
    difficulties = Counter(str(record.get("difficulty", "<missing>")) for record in records)

    print(f"Checked: {input_path}")
    print(f"Samples: {len(records)}")
    print("Categories: " + format_counts(categories))
    print("Difficulties: " + format_counts(difficulties))

    if errors:
        print(f"Errors: {len(errors)}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Result: valid")
    return 0


def format_counts(counts: Counter[str]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the Golden Set JSONL file.")
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_INPUT_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return check_golden(args.path)


if __name__ == "__main__":
    raise SystemExit(main())
