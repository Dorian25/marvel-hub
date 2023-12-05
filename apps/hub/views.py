from django.shortcuts import render
from ..comics.models import Series
from ..comics.models import Issue
from ..movies.models import Movie
from ..characters.models import Character

# Create your views here.
def start_hub(request):
    # TODO
    # HOT SERIES
    #hot_series = Series.objects.all().order_by("-hit_count_generic__hits")
    # HOT MOVIES
    #hot_movies = Movie.objects.all().order_by("-hit_count_generic__hits")
    # HOT CHARACTERS
    #hot_characters = []
    # HOT ISSUES
    #hot_issues = Issue.objects.all().order_by("-hit_count_generic__hits")

    return render(request, 'hub/home.html', {"hot_series": [],
                                             "hot_movies": [],
                                             "hot_issues": [],
                                             "hot_characters": []})