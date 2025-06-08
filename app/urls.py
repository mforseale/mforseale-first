from django.urls import path
from .views import live_search, AjaxSearchView, HomePageView, MovieListView, ListView, UserListView, ReviewListView, MovieDetailView,SearchView,AddReviewView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('movies/', MovieListView.as_view(), name='movies'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('lists/', ListView.as_view(), name='lists'),
    path('users/', UserListView.as_view(), name='users'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('movies/search/', SearchView.as_view(), name='search'),
    path('movies/<int:pk>/add_review/', AddReviewView.as_view(), name='add_review'),
    path('search/', SearchView.as_view(), name='search_results'),
    path('ajax/search/', AjaxSearchView.as_view(), name='ajax_search'),
    path("live-search/", live_search, name="live_search"),

]
