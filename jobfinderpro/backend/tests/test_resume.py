from pathlib import Path
from app.services.resume import extract_keywords, get_resume_keywords

SAMPLE_TEXT = """
John Doe
Senior Software Engineer

Skills: Python, FastAPI, SQLAlchemy, Postgres, JavaScript (JS), React, TypeScript (TS), Docker, AWS, GitHub Actions
Experience building REST and GraphQL APIs. Deployed on Kubernetes.
"""

def test_extract_keywords_from_text():
    keywords = extract_keywords(SAMPLE_TEXT)
    # Ensure core tokens are present
    for expected in ["python", "fastapi", "sqlalchemy", "postgres", "react", "typescript", "javascript", "docker", "aws", "github actions"]:
        assert expected in keywords
    # Synonym expansion: js -> javascript, ts -> typescript already normalized
    assert "javascript" in keywords
    assert "typescript" in keywords


def test_get_resume_keywords_from_txt(tmp_path: Path):
    p = tmp_path / "resume.txt"
    p.write_text(SAMPLE_TEXT)
    keywords = get_resume_keywords(p)
    assert len(keywords) >= 8