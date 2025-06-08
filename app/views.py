from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from app.models import Movie, List, User, Review
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.views.generic import ListView
from django.db.models import Q
from .models import Movie

class SearchView(ListView):
    template_name = "movies.html"
    model = Movie
    context_object_name = "movies"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Movie.objects.filter(
                Q(title__icontains=query) |
                Q(director__icontains=query) |
                Q(release_year__istartswith=query)
            ).order_by("-release_year")
        return Movie.objects.all().order_by("-release_year")


class HomePageView(TemplateView):
    template_name = 'home.html'

class MovieListView(ListView):
    template_name = 'movies.html'
    model = Movie
    context_object_name = "movies"


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = self.object
            review.user = request.user
            review.save()
            return redirect('movie_detail', pk=self.object.pk)

        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # --- учёт просмотров ---
        viewed_movies = request.session.get('viewed_movies', [])
        movie_id = self.object.pk

        if movie_id not in viewed_movies:
            self.object.view_count += 1
            self.object.save()
            viewed_movies.append(movie_id)
            request.session['viewed_movies'] = viewed_movies
            request.session.modified = True

        return self.render_to_response(context)
# views.py
from django.views.generic.edit import FormView
from .forms import ReviewForm

class AddReviewView(FormView):
    form_class = ReviewForm

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        review.movie_id = self.kwargs['pk']
        review.save()
        return redirect('movie_detail', pk=self.kwargs['pk'])

class ListView(ListView):
    template_name = 'lists.html'
    model = List
    context_object_name = "lists"

class UserListView(ListView):
    template_name = 'users.html'
    model = User
    context_object_name = "users"  # Правильное имя переменной

    def get_queryset(self):
        return User.objects.all()

class ReviewListView(ListView):
    template_name = 'reviews.html'
    model = Review
    context_object_name = "reviews"
from django.shortcuts import render, get_object_or_404
from .models import Movie

# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Review  # или где хранятся рецензии

@login_required
def profile_view(request):
    reviews = Review.objects.filter(user=request.user).select_related('movie').order_by('-created_at')
    return render(request, 'profile.html', {'reviews': reviews})



from django.shortcuts import render
from .models import Movie
from django.db.models import Q

class SearchView(ListView):
    model = Movie
    template_name = "search_results.html"
    context_object_name = "movies"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Movie.objects.filter(title__icontains=query) | Movie.objects.filter(director__icontains=query)
from django.http import JsonResponse
from django.views import View
from app.models import Movie  # или где у тебя модель

from django.http import JsonResponse
from app.models import Movie

from django.http import JsonResponse
from django.views import View
from .models import Movie

class AjaxSearchView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        movies = Movie.objects.filter(title__icontains=query) | Movie.objects.filter(director__icontains=query)
        data = [
            {
                "movie_id": movie.movie_id,
                "title": movie.title,
                "poster_url": movie.poster_url,
                "director": movie.director,
                "genre": movie.genre,
                "rating": movie.rating,
                "popularity": movie.popularity,
                "release_year": movie.release_year,
            }
            for movie in movies
        ]
        return JsonResponse(data, safe=False)


def live_search(request):
    q = request.GET.get("q", "")
    results = Movie.objects.filter(title__icontains=q)[:10]
    data = {"results": [{"id": movie.id, "title": movie.title, "release_year": movie.release_year} for movie in results]}
    return JsonResponse(data)
# views.py
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile, Movie


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile, Review

@login_required
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    reviews = profile.user.review_set.all()  # если модель Review с ForeignKey на user
    rated_movies = profile.favorite_movies.all()  # или по-другому, если ты хранишь оценки отдельно

    return render(request, 'profile.html', {
        'profile': profile,
        'reviews': reviews,
        'rated_movies': rated_movies
    })
    user = request.user
    rated_movies = Rating.objects.filter(user=user).count()
    ratings = Rating.objects.filter(user=user).values_list('score', flat=True)

    distribution = {}
    for i in range(1, 11):
        distribution[i] = ratings.filter(score=i).count()

    context = {
        'user_stats': {
            'rated_movies': rated_movies,
            'rating_distribution': distribution,
        }
    }
    return render(request, 'profile.html', context)


from django.shortcuts import get_object_or_404, redirect, render  # Добавлен render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Rating, Movie
from .forms import RatingForm

from django.http import JsonResponse
from django.views.decorators.http import require_POST


@require_POST
def rate_movie(request, movie_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Требуется авторизация'})

    try:
        movie = Movie.objects.get(pk=movie_id)
        score = int(request.POST.get('score'))

        if not (2 <= score <= 10):
            return JsonResponse({'success': False, 'error': 'Некорректная оценка'})

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'score': score}
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@require_POST
def toggle_favorite(request, movie_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Требуется авторизация'})

    try:
        movie = Movie.objects.get(pk=movie_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            movie=movie
        )

        if not created:
            favorite.delete()
            return JsonResponse({'success': True, 'action': 'removed'})

        return JsonResponse({'success': True, 'action': 'added'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
def movie_list(request):
    movies = Movie.objects.all().prefetch_related('user_ratings', 'favorites')
    return render(request, 'movies.html', {'movies': movies})