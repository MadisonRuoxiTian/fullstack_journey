from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "documents.jsonl"
REPORT_PATH = PROJECT_ROOT / "reports" / "quality_report.md"
SHORT_TEXT_LIMIT = 20


def load_documents() -> list[dict]:
    documents = []
    with INPUT_PATH.open(encoding="utf-8") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            try:
                document = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON on line {line_number}: {error.msg}") from error

            if not isinstance(document, dict) or not isinstance(document.get("text"), str):
                raise ValueError(f"Invalid document on line {line_number}: expected a string 'text' field")

            documents.append(document)
    return documents


def source_path(document: dict) -> str:
    return str(document.get("source_path", "<unknown source>"))


def build_report(documents: list[dict]) -> str:
    lengths = [len(document["text"]) for document in documents]
    empty_documents = [document for document in documents if not document["text"].strip()]
    short_documents = [document for document in documents if 0 < len(document["text"]) < SHORT_TEXT_LIMIT]

    documents_by_text: dict[str, list[dict]] = defaultdict(list)
    for document in documents:
        documents_by_text[document["text"]].append(document)
    duplicate_groups = [group for group in documents_by_text.values() if len(group) > 1]
    duplicate_count = sum(len(group) - 1 for group in duplicate_groups)

    lines = [
        "# Dataset Quality Report",
        "",
        "## Summary",
        "",
        f"- Total documents: {len(documents)}",
        f"- Empty-text documents: {len(empty_documents)}",
        f"- Exact duplicate documents: {duplicate_count}",
        f"- Short-text documents (< {SHORT_TEXT_LIMIT} characters): {len(short_documents)}",
        f"- Minimum text length: {min(lengths, default=0)} characters",
        f"- Maximum text length: {max(lengths, default=0)} characters",
        f"- Average text length: {mean(lengths) if lengths else 0:.2f} characters",
        "",
        "## Issues",
        "",
    ]

    if not empty_documents and not short_documents and not duplicate_groups:
        lines.append("No empty texts, short texts, or exact duplicate texts were found.")
    else:
        if empty_documents:
            lines.extend(["### Empty-text documents", ""])
            lines.extend(f"- {source_path(document)}" for document in empty_documents)
            lines.append("")
        if short_documents:
            lines.extend([f"### Short-text documents (< {SHORT_TEXT_LIMIT} characters)", ""])
            lines.extend(f"- {source_path(document)} ({len(document['text'])} characters)" for document in short_documents)
            lines.append("")
        if duplicate_groups:
            lines.extend(["### Exact duplicate groups", ""])
            for group in duplicate_groups:
                lines.append("- " + "; ".join(source_path(document) for document in group))

    return "\n".join(lines) + "\n"


def main() -> None:
    documents = load_documents()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(documents), encoding="utf-8")
    print(f"Wrote quality report to {REPORT_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
