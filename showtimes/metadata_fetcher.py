# Helper functions to get movie information from IMDb
# Using: https://github.com/tveronesi/imdbinfo

from imdbinfo import search_title
from .models import Movie

def search_movies(search_text):
    results = search_title(search_text)
    return [
        Movie(
            title=movie.title,
            year=movie.year,
            cover_url=movie.cover_url, 
        ) for movie in results.titles
        if not movie.is_series()
    ]
# Note: models can be used without saving: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Models#model_management
