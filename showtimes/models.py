from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    showed_at = models.DateField(null=True, blank=True)
    cover_url = models.URLField(default='/static/showtimes/images/no-cover.jpg')
    year = models.IntegerField(default=0)
    description = models.TextField(default='No description')

    def __str__(self):
        return f"{self.title} ({self.vote_count} votes)"
    
    # @property
    # def upcoming(self):
    #     return self.showed_at is None
    
    # @property
    # def previously_shown(self):
    #     return self.showed_at is not None

