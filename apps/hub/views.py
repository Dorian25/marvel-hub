from django.shortcuts import render
from ..comics.models import Series
from ..comics.models import Issue
from ..movies.models import Movie
from ..characters.models import Character

# Create your views here.
def start_hub(request):
    # HOT SERIES
    hot_series = Series.objects.order_by("hit_count_generic__hits").reverse()[:10]
    # HOT MOVIES
    hot_movies = Movie.objects.order_by("hit_count_generic__hits").reverse()[:10]
    # HOT CHARACTERS
    hot_characters = []
    # HOT ISSUES
    hot_issues = []

    return render(request, 'hub/home.html', {"hot_series": hot_series,
                                             "hot_movies": hot_movies,
                                             "hot_issues": hot_issues,
                                             "hot_characters": hot_characters})