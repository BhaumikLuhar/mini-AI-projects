from pathlib import Path

PROJECT_ROOT=Path.cwd()

DEFAULT_DOCS_DIR = PROJECT_ROOT / "docs"

DEFAULT_INDEX_STATE = (
    PROJECT_ROOT / "index_state.json"
)

DEFAULT_CHROMA_DIR = (
    PROJECT_ROOT / "chroma_data"
)