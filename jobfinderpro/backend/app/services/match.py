from __future__ import annotations
from typing import List, Set, Tuple
import re

_TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9+_.#-]{1,}")


def _normalize_tokens(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN_PATTERN.findall(text or "")]


def _compute_overlap_score(resume_keywords: Set[str], job_text: str) -> float:
    if not resume_keywords:
        return 0.0
    job_tokens = set(_normalize_tokens(job_text))
    if not job_tokens:
        return 0.0
    intersect = resume_keywords.intersection(job_tokens)
    return len(intersect) / max(1, len(resume_keywords))


def _tfidf_cosine_similarity(resume_doc: str, job_doc: str) -> float:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
        from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
    except Exception:
        # Fallback: simple Jaccard similarity as a very rough proxy
        resume_tokens = set(_normalize_tokens(resume_doc))
        job_tokens = set(_normalize_tokens(job_doc))
        if not resume_tokens or not job_tokens:
            return 0.0
        intersection = len(resume_tokens & job_tokens)
        union = len(resume_tokens | job_tokens)
        return intersection / union

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_doc, job_doc])
    sim_matrix = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return float(sim_matrix[0, 0])


def compute_match_score(resume_keywords: List[str], job_text: str, *, weight_tfidf: float = 0.7, weight_overlap: float = 0.3) -> Tuple[float, float, float]:
    """
    Returns a tuple: (final_score_0_100, tfidf_component_0_100, overlap_component_0_100)
    """
    clean_keywords = [k.strip().lower() for k in resume_keywords if k and k.strip()]
    resume_doc = " ".join(sorted(set(clean_keywords)))
    tfidf_sim = _tfidf_cosine_similarity(resume_doc, job_text)
    overlap = _compute_overlap_score(set(clean_keywords), job_text)

    final_score = (weight_tfidf * tfidf_sim + weight_overlap * overlap) * 100.0
    # Clamp and round to 2 decimals for stability
    final_score = max(0.0, min(100.0, final_score))
    return round(final_score, 2), round(tfidf_sim * 100.0, 2), round(overlap * 100.0, 2)