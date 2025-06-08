from django.db import models
from django.contrib.auth.models import User



class Movie(models.Model):
    movie_id = models.AutoField("ID", primary_key=True)
    title = models.CharField("Title", max_length=255)
    director = models.CharField("Director", max_length=255)
    description = models.TextField("Description")
    duration = models.PositiveIntegerField("Duration (minutes)")
    genre = models.CharField("Genre", max_length=100)
    rating = models.FloatField("Rating", default=0.0)
    release_year = models.PositiveIntegerField("Release Year")
    popularity = models.IntegerField("Popularity", default=0)
    view_count = models.PositiveIntegerField(default=0)
    poster_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Ссылка на постер (URL). Например: https://image.tmdb.org/t/p/w500/abc.jpg"
    )
    def __str__(self):
        return self.title


class Review(models.Model):
    review_id = models.AutoField("ID", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField("Review Text")
    rating = models.PositiveIntegerField("Rating", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"


class List(models.Model):
    list_id = models.AutoField("ID", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    name = models.CharField("List Name", max_length=255)
    movies = models.ManyToManyField(Movie, related_name='lists')

    def __str__(self):
        return f"{self.name} by {self.user.username}"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    favorite_movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return self.user.username


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_ratings')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # Оценка от 1 до 10

    class Meta:
        unique_together = ('user', 'movie')  # Один пользователь - одна оценка на фильм
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title} as {self.score}"

    def save(self, *args, **kwargs):
        # Проверяем, что оценка в допустимом диапазоне
        if not 1 <= self.score <= 10:
            raise ValueError("Score must be between 1 and 10")
        super().save(*args, **kwargs)

        # Обновляем средний рейтинг фильма
        self.update_movie_rating()

    def update_movie_rating(self):
        ratings = Rating.objects.filter(movie=self.movie)
        count = ratings.count()
        total = sum(r.score for r in ratings)
        self.movie.rating = total / count if count > 0 else 0
        self.movie.save()
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favorites')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='favorites')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')