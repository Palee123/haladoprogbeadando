from flask import session
from tmdb import safe_tmdb_request, get_tmdb_language, get_tmdb_api_key


def get_similar_movies_local(movie_id, limit=10):
    params = {
        "api_key": get_tmdb_api_key(),
        "language": get_tmdb_language(),
        "region": "HU" if session.get("lang") == "hu" else "US",
    }

    data = safe_tmdb_request(
        f"movie/{movie_id}/similar",
        params=params,
        fallback={"results": []}
    )

    return data.get("results", [])[:limit]


def recommend_for_user(favorite_movie_ids):
    if not favorite_movie_ids:
        return []

    ref_id = favorite_movie_ids[0]

    similar = get_similar_movies_local(ref_id, limit=10)

    result = [m for m in similar if m.get("id") != ref_id]

    return result
