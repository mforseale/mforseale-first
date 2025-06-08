from django.contrib import admin
from .models import Movie, Review, List
admin.site.register(Movie)
admin.site.register(Review)
@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'movies_count')

    def movies_count(self, obj):
        return obj.movies.count()

    movies_count.short_description = 'Number of Movies'