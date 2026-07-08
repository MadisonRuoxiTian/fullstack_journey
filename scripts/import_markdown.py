from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "documents.jsonl"
SUPPORTED_SUFFIXES = {".md", ".txt"}


def file_type_for(path: Path) -> str:
    if path.suffix.lower() == ".md":
        return "markdown"
    return "text"


def iter_source_files() -> list[Path]:
    return sorted(
        path
        for path in RAW_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def build_record(index: int, path: Path, text: str) -> dict:
    return {
        "id": f"doc_{index:04d}",
        "source_path": path.relative_to(PROJECT_ROOT).as_posix(),
        "title": path.stem,
        "text": text,
        "metadata": {
            "file_type": file_type_for(path),
        },
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    imported_count = 0
    with OUTPUT_PATH.open("w", encoding="utf-8") as output_file:
        for source_path in iter_source_files():
            text = source_path.read_text(encoding="utf-8").strip()
            if not text:
                continue

            imported_count += 1
            record = build_record(imported_count, source_path, text)
            output_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Imported {imported_count} documents to {OUTPUT_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
