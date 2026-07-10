from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "documents.jsonl"
SUPPORTED_SUFFIXES = {".md", ".txt"}


def file_type_for(path: Path) -> str:
    if path.suffix.lower() == ".md":
        return "markdown"
    return "text"


def iter_source_files(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def build_record(index: int, path: Path, text: str, project_root: Path = PROJECT_ROOT) -> dict:
    return {
        "id": f"doc_{index:04d}",
        "source_path": path.relative_to(project_root).as_posix(),
        "title": path.stem,
        "text": text,
        "metadata": {
            "file_type": file_type_for(path),
        },
    }


def import_documents(input_dir: Path, output_path: Path, project_root: Path = PROJECT_ROOT) -> int:
    input_dir = input_dir.resolve()
    output_path = output_path.resolve()
    project_root = project_root.resolve()
    if not input_dir.is_dir():
        print(f"Error: input directory does not exist: {input_dir}", file=sys.stderr)
        return 1

    imported_count = 0
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as output_file:
            for source_path in iter_source_files(input_dir):
                try:
                    text = source_path.read_text(encoding="utf-8").strip()
                except UnicodeDecodeError:
                    print(f"Warning: skipped non-UTF-8 file: {source_path}", file=sys.stderr)
                    continue
                if not text:
                    continue

                imported_count += 1
                record = build_record(imported_count, source_path, text, project_root)
                output_file.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as error:
        print(f"Error: failed to write output file {output_path}: {error}", file=sys.stderr)
        return 1

    print(f"Imported {imported_count} documents to {output_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Markdown and text files into JSONL.")
    parser.add_argument("--input", type=Path, default=RAW_DIR, help="Directory containing .md or .txt files.")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH, help="Destination JSONL file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return import_documents(args.input, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
