from django.urls import path
from . import views

urlpatterns = [
    path('', views.upcoming_movies, name='upcoming_movies'),
    path('previously-shown/', views.previously_shown, name='previously_shown'),
    path('add/', views.add_movie, name='add_movie'),
    path('vote/<int:movie_id>/', views.vote_movie, name='vote_movie'),
    path('mark-as-shown/<int:movie_id>/', views.mark_as_shown, name='mark_as_shown'),
]
