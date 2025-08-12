from app.services.match import compute_match_score

resume_keywords = [
    "python", "fastapi", "sqlalchemy", "postgres", "react", "typescript", "docker", "aws"
]


def test_match_score_prefers_richer_job_description():
    job_text_low = "We use Java and Spring. SQL experience nice to have."
    job_text_high = (
        "Looking for a Python engineer with FastAPI, SQLAlchemy, and Postgres. "
        "Experience with React and TypeScript on the frontend, Docker, and AWS."
    )

    score_low, tfidf_low, overlap_low = compute_match_score(resume_keywords, job_text_low)
    score_high, tfidf_high, overlap_high = compute_match_score(resume_keywords, job_text_high)

    assert score_high > score_low
    assert tfidf_high >= tfidf_low
    assert overlap_high >= overlap_low