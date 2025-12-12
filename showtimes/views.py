from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from .models import Movie
from .metadata_fetcher import search_movies as imdb_search


def upcoming_movies(request):
    movies = Movie.objects.filter(showed_at__isnull=True).order_by('-vote_count', 'created_at')
    search_results = None
    search_query = ''

    if request.method == 'POST' and 'search' in request.POST:
        search_query = request.POST.get('title', '').strip()
        if search_query:
            search_results = imdb_search(search_query)

    return render(request, 'showtimes/upcoming.html', {
        'movies': movies,
        'search_results': search_results,
        'search_query': search_query,
    })

    # return render(request, 'showtimes/upcoming.html', {'movies': movies})



def previously_shown(request):
    movies = Movie.objects.filter(showed_at__isnull=False).order_by('-showed_at')
    return render(request, 'showtimes/previously_shown.html', {'movies': movies})


def add_movie(request):
    if request.method == 'POST':
        # TODO i'll edit this later
        title = request.POST.get('title', '').strip()
        year = request.POST.get('year', '')
        cover_url = request.POST.get('cover_url', '')
        description = request.POST.get('description', '')

        if title:
            movie_data = {'title': title}
            if year:
                movie_data['year'] = int(year)
            if cover_url:
                movie_data['cover_url'] = cover_url
            if description:
                movie_data['description'] = description

            Movie.objects.create(**movie_data)
            messages.success(request, f'Movie "{title}" added successfully!')
        else:
            messages.error(request, 'Please enter a movie title.')
    return redirect('upcoming_movies')


def vote_movie(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        movie.vote_count += 1
        movie.save()
        messages.success(request, f'Voted for "{movie.title}"!')
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
