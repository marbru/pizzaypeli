# Helper functions to get movie information from IMDb
# Using: https://github.com/tveronesi/imdbinfo

from imdbinfo import get_movie, search_title

def search_movies(search_text):
    results = search_title(search_text)
    return [
        {
            'title': movie.title, 
            'year': movie.year, 
            'cover_url': movie.cover_url,
            'imdb_id': movie.imdb_id
        }
        for movie in results.titles
        if not movie.is_series()
    ]

def get_movie_info(imdb_id):
    movie = get_movie(imdb_id)
    return {
        'title': movie.title,
        'year': movie.year,
        'cover_url': movie.cover_url,
        # 'imdb_id': movie.imdb_id,
        'description': movie.plot
    }