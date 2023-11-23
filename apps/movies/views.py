from django.shortcuts import render
from .models import Movie
from django.core.paginator import Paginator
from django.http import JsonResponse
import os
import requests

# Create your views here.
def home(request):
    page = request.GET.get('page', 1) # default value 1
    all_movies = Movie.objects.all().order_by('-release_date') # "-" order desc
    paginator = Paginator(all_movies, 20) # Show 20 series per page
    list_movies = paginator.get_page(page)
    list_movies.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(request, 'movies/home.html', {"number_movies": len(all_movies),
                                                "list_movies":list_movies})

def get_movie(request, pk):          
    try:
        movie = Movie.objects.get(movie_id=pk)
    except Movie.DoesNotExist:
        return render(request, './404error.html')

    return render(request, 'movies/get_movie.html', {"movie": movie})

def get_rapid_api_imdb_id(request):
    pass

def get_rapid_api_imdb_data(request):
    pass
    """
    url = "https://mdblist.p.rapidapi.com/"
    imdb_response = {}
    querystring = {"s":movie.name,
                   "y":movie.release_date.year,
                   "m":"movie",
                   "l":"1"}
    headers = {
        "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
        "X-RapidAPI-Host": "mdblist.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    jsonresponse = response.json()

    if jsonresponse["response"] and jsonresponse["total"] == 1:
        imdb_id = jsonresponse["search"][0]["id"]

        querystring = {"i":imdb_id}

        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "mdblist.p.rapidapi.com"
        }

        imdb_response = requests.get(url, headers=headers, params=querystring).json()

    return JsonResponse(results, safe=False)
    """

def ajax_search(request):
    if 'term' in request.GET:
        movies = Movie.objects.filter(name__istartswith = request.GET.get('term'))
        results = [{"name":movie.name,
                    "movie_id":movie.movie_id} for movie in movies]
        return JsonResponse(results, safe=False)