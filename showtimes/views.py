from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from .models import Movie
from . import imdb


def upcoming_movies(request):
    all_movies = Movie.objects.all()  # we shouldn't have that many, so this is ok
    upcoming_movies = all_movies.filter(showed_at__isnull=True).order_by('-vote_count', 'created_at')

    # Compute search results if we have search input
    search_results = None
    search_query = ''
    if request.method == 'POST' and 'search' in request.POST:
        search_query = request.POST.get('title', '').strip()
        if search_query:
            search_results = imdb.search_movies(search_query)
        for result_movie in (search_results or []):
            # Not sure if this'll be a lot of DB calls 
            existing_movie = all_movies.filter(imdb_id=result_movie['imdb_id']).first()
            if existing_movie:
                result_movie['existing_id'] = existing_movie.id
                result_movie['is_upcoming'] = existing_movie.is_upcoming
                result_movie['is_previously_shown'] = existing_movie.is_previously_shown

    return render(request, 'showtimes/upcoming.html', {
        'upcoming_movies': upcoming_movies,
        'search_results': search_results,
        'search_query': search_query,
    })


def previously_shown(request):
    movies = Movie.objects.filter(showed_at__isnull=False).order_by('-showed_at')
    return render(request, 'showtimes/previously_shown.html', {'movies': movies})


def add_movie(request):
    if request.method == 'POST':
        imdb_id = request.POST.get('imdb_id', '').strip()
        try:
            movie_data = imdb.get_movie_info(imdb_id)
            movie = Movie.objects.create(**movie_data)
            messages.success(request, f'Added "{movie.title}"')
        except Exception:
            messages.error(request, 'Could not add movie. Please try again later.')

    return redirect('upcoming_movies')


def vote_movie(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        movie.vote_count += 1
        movie.save()
        messages.success(request, f'Voted for "{movie.title}"')
    return redirect('upcoming_movies')


def mark_as_shown(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        showed_date = request.POST.get('showed_date')
        if showed_date:
            movie.showed_at = showed_date
            movie.save()
            messages.success(request, f'Marked "{movie.title}" as shown on {showed_date}!')
        else:
            messages.error(request, 'Please select a date.')
    return redirect('upcoming_movies')


def delete_movie(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        title = movie.title
        movie.delete()
        messages.success(request, f'Deleted "{title}"')
    return redirect('upcoming_movies')
