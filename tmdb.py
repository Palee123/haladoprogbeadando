import requests
from flask import current_app, session


def get_tmdb_api_key():
    return current_app.config.get("TMDB_API_KEY")


def get_tmdb_base_url():
    return current_app.config.get("TMDB_BASE_URL", "https://api.themoviedb.org/3")


def get_tmdb_language():
    return "hu-HU" if session.get("lang", "hu") == "hu" else "en-US"


def safe_tmdb_request(endpoint, params=None, fallback=None):
    if params is None:
        params = {}

    url = f"{get_tmdb_base_url()}/{endpoint}"

    params.update({
        "api_key": get_tmdb_api_key()
    })

    try:
        response = requests.get(url, params=params, timeout=5)
        return response.json()
    except Exception:
        return fallback or {}
    


# POPULAR MOVIES

def get_popular_movies():
    data = safe_tmdb_request(
        "movie/popular",
        params={"language": get_tmdb_language()},
        fallback={"results": []}
    )
    return data.get("results", [])



# MOVIE DETAILS

def get_movie_details(movie_id):
    data = safe_tmdb_request(
        f"movie/{movie_id}",
        params={"language": get_tmdb_language()},
        fallback={}
    )
    return data



# GENRE LIST

def get_genres():
    data = safe_tmdb_request(
        "genre/movie/list",
        params={"language": get_tmdb_language()},
        fallback={"genres": []}
    )
    return data.get("genres", [])



# SIMILAR MOVIES (belső egységes hívás)

def _tmdb_similar_request(movie_id, limit=10):
    data = safe_tmdb_request(
        f"movie/{movie_id}/recommendations",
        params={
            "language": "en-US",
            "region": "en-US"
        },
        fallback={"results": []}
    )

    return data.get("results", [])[:limit]


def get_similar_movies_api(movie_id, limit=10):
    return _tmdb_similar_request(movie_id, limit)
