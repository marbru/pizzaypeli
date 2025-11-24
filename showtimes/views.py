from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from .models import Movie


def upcoming_movies(request):
    movies = Movie.objects.filter(showed_at__isnull=True)
    return render(request, 'showtimes/upcoming.html', {'movies': movies})


def previously_shown(request):
    movies = Movie.objects.filter(showed_at__isnull=False).order_by('-showed_at')
    return render(request, 'showtimes/previously_shown.html', {'movies': movies})


def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Movie.objects.create(title=title)
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
