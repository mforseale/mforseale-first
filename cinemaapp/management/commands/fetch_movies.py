from django.core.management.base import BaseCommand
import requests
from app.models import Movie  # замените 'app' на имя вашего приложения

API_KEY = 'b546f083bd6acedb7ad73b5e42cb4b7c'  # ← вставь сюда свой настоящий API ключ

class Command(BaseCommand):
    help = 'Fetches movies from TMDb API and saves to DB'

    def handle(self, *args, **kwargs):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1'
        response = requests.get(url)
        data = response.json()

        for movie_data in data.get('results', []):
            Movie.objects.update_or_create(
                title=movie_data.get('title', ''),
                defaults={
                    'description': movie_data.get('overview', ''),
                    'rating': movie_data.get('vote_average', 0.0),
                    'release_year': int(movie_data.get('release_date', '0000')[:4] or 0),
                    'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}" if movie_data.get('poster_path') else '',
                    'genre': 'Unknown',
                    'duration': 90,
                    'popularity': int(movie_data.get('popularity', 0)),
                    'view_count': int(movie_data.get('vote_count', 0)),
                    'director': 'Unknown',
                }
            )

        self.stdout.write(self.style.SUCCESS("🎉 Фильмы успешно загружены в базу данных!"))
