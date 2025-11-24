from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    showed_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-vote_count', 'title']

    def __str__(self):
        return f"{self.title} ({self.vote_count} votes)"

    @property
    def is_shown(self):
        return self.showed_at is not None
