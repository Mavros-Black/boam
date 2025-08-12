from __future__ import annotations
from pathlib import Path
from typing import Iterable, List, Set
import re

# Optional imports guarded for runtime
try:
    import docx  # type: ignore
except Exception:  # pragma: no cover
    docx = None

try:
    from pypdf import PdfReader  # type: ignore
except Exception:  # pragma: no cover
    PdfReader = None


SYNONYMS = {
    "js": ["javascript"],
    "javascript": ["js"],
    "ts": ["typescript"],
    "typescript": ["ts"],
    "node": ["node.js", "nodejs"],
    "node.js": ["node", "nodejs"],
    "postgresql": ["postgres"],
    "postgres": ["postgresql"],
    "aws": ["amazon web services"],
    "gh actions": ["github actions"],
}

TECH_TOKENS = {
    # common web
    "javascript", "typescript", "react", "next", "vite", "tailwind",
    "node", "node.js", "express", "graphql", "rest", "docker", "kubernetes",
    # backend & data
    "python", "fastapi", "django", "flask", "sqlalchemy", "alembic",
    "postgres", "postgresql", "mysql", "sqlite", "redis", "kafka",
    # cloud & devops
    "aws", "gcp", "azure", "terraform", "ansible",
}

# Known multi-word tokens to detect directly in text
MULTIWORD_TOKENS = {
    "github actions",
}

TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9+_.#-]{1,}")


def _read_text_from_pdf(path: Path) -> str:
    if PdfReader is None:
        raise RuntimeError("pypdf not installed")
    reader = PdfReader(str(path))
    chunks: List[str] = []
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
    return "\n".join(chunks)


def _read_text_from_docx(path: Path) -> str:
    if docx is None:
        raise RuntimeError("python-docx not installed")
    d = docx.Document(str(path))
    return "\n".join(p.text or "" for p in d.paragraphs)


def _read_text_from_plain(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _normalize_tokens(text: str) -> List[str]:
    tokens = [t.lower() for t in TOKEN_PATTERN.findall(text)]
    return tokens


def _expand_synonyms(tokens: Iterable[str]) -> Set[str]:
    expanded: Set[str] = set(tokens)
    for token in list(expanded):
        if token in SYNONYMS:
            expanded.update(SYNONYMS[token])
    return expanded


def extract_keywords(text: str) -> List[str]:
    # Include multiword tokens by scanning the raw text lowercased
    lowered = text.lower()
    multi = {mw for mw in MULTIWORD_TOKENS if mw in lowered}

    tokens = _normalize_tokens(text)
    candidates = {t for t in tokens if t in TECH_TOKENS}
    expanded = _expand_synonyms(candidates)
    expanded.update(multi)
    # remove duplicates while keeping a stable sort (alphabetical)
    return sorted(expanded)


def get_resume_keywords(path: str | Path) -> List[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Resume file not found: {p}")

    suffix = p.suffix.lower()
    if suffix == ".pdf":
        text = _read_text_from_pdf(p)
    elif suffix == ".docx":
        text = _read_text_from_docx(p)
    else:
        text = _read_text_from_plain(p)

    return extract_keywords(text)