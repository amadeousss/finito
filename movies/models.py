from django.db import models
from django.conf import settings


class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imdb_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    release_date = models.CharField(max_length=15)
    runtime = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    minutes_seen = models.IntegerField()
    is_fully_seen = models.BooleanField(default=False)
    poster_url = models.URLField()

    @property
    def minutes_seen_formatted(self):
        return f"{self.minutes_seen // 60}h {self.minutes_seen % 60}min"

    @property
    def percent_seen(self):
        return f"{round(self.minutes_seen / self.runtime * 100)}"

    @property
    def runtime_formatted(self):
        return f"{self.runtime // 60}h {self.runtime % 60}min"

    @property
    def release_year(self):
        return self.release_date[-4:]

    def __str__(self):
        return f"{self.title} ({list(self.release_date)[-1]})"
