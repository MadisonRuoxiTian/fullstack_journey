import importlib.util
import json
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "import_markdown.py"
SPEC = importlib.util.spec_from_file_location("import_markdown", SCRIPT_PATH)
import_markdown = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(import_markdown)


def test_imports_non_empty_markdown_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "data" / "raw"
    input_dir.mkdir(parents=True)
    (input_dir / "note.md").write_text("# Title\n\nContent", encoding="utf-8")
    output_path = tmp_path / "data" / "processed" / "documents.jsonl"

    exit_code = import_markdown.import_documents(input_dir, output_path, tmp_path)

    assert exit_code == 0
    documents = [json.loads(line) for line in output_path.read_text(encoding="utf-8").splitlines()]
    assert documents == [{"id": "doc_0001", "source_path": "data/raw/note.md", "title": "note", "text": "# Title\n\nContent", "metadata": {"file_type": "markdown"}}]


def test_empty_directory_creates_empty_jsonl(tmp_path: Path) -> None:
    input_dir = tmp_path / "data" / "raw"
    input_dir.mkdir(parents=True)
    output_path = tmp_path / "data" / "processed" / "documents.jsonl"

    exit_code = import_markdown.import_documents(input_dir, output_path, tmp_path)

    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8") == ""


def test_missing_input_directory_returns_error(tmp_path: Path, capsys) -> None:
    missing_input_dir = tmp_path / "missing"
    output_path = tmp_path / "data" / "processed" / "documents.jsonl"

    exit_code = import_markdown.import_documents(missing_input_dir, output_path, tmp_path)

    assert exit_code == 1
    assert "input directory does not exist" in capsys.readouterr().err
    assert not output_path.exists()