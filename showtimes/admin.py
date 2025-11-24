from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'vote_count', 'showed_at', 'created_at']
    list_filter = ['showed_at', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at']
