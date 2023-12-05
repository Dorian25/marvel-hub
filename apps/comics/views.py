from django.shortcuts import render
from django.http import Http404
from .models import Series
from .models import Issue
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
import re
import binascii
import cloudscraper
from django.http import JsonResponse

def home(request):
    return render(request, "comics/home.html", {})

def home_series(request):
    # FEATURED SERIES
    # TODO
    featured_series_filter = ['Eternals Vol 3 (2006–2007)', 'Black Widow Vol 5 (2014–2015)', 'Avengers Vol 8 (2018–2023)', 
                              'Infinity Gauntlet Vol 1 (1991)', 'Amazing Spider-Man Vol 5 (2018–2022)',
                              'Star Wars Vol 2 (2015–2020)', 'Ms. Marvel Vol 4 (2016–2019)', 'Moon Knight Vol 7 (2014–2015)',
                              'Vision Vol 2 (2016)']
    featured_series = Series.objects.filter(rawname__in=featured_series_filter)
    # ALL SERIES
    page = request.GET.get('page', 1)
    all_series = Series.objects.all().order_by('cleanname')
    paginator = Paginator(all_series, 20) # Show 20 series per page
    list_series = paginator.get_page(page)
    list_series.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(request, 'comics/series.html', {"number_series": len(all_series),
                                                  "list_series": list_series,
                                                  "featured_series": featured_series})

def get_series(request, pk):
    try:
        series = Series.objects.get(series_id=pk)
    except Series.DoesNotExist:
        return render(request, './404error.html')
    
    issues = Issue.objects.filter(series_id=pk)

    return render(request, 'comics/get_series.html', {"series": series, "issues": issues})

def get_issue(request, pk):
    try:
        issue = Issue.objects.get(issue_id=pk)
    except Issue.DoesNotExist:
        return render(request, './404error.html')
    
    # get url_read
    url = issue.url_read

    if url != "NA":
        pages = []
        try :
            scraper = cloudscraper.create_scraper()
            soup = BeautifulSoup(scraper.get(url).text, "html.parser")

            valid_script = soup.find(lambda tag:tag.name=="script" and "lstImages.push" in tag.text)
            chapter_images_regex = r"lstImages\.push\([\"'](.*)[\"']\)"
            matches = re.findall(chapter_images_regex, valid_script.text)

            def beau(url):
                # url is crypted by a function in Scripts/rguard.min.js?v=1.2.9
                # https://github.com/Xonshiz/comic-dl/issues/299
                # https://github.com/Xonshiz/comic-dl/pull/344/files
                url = url.replace("_x236", "d").replace("_x945", "g")

                if url.startswith("https"):
                    return url

                url, sep, rest = url.partition("?")
                containsS0 = "=s0" in url
                url = url[:-3 if containsS0 else -6]
                url = url[4:22] + url[25:]
                url = url[0:-6] + url[-2:]
                url = binascii.a2b_base64(url).decode()
                url = url[0:13] + url[17:]
        
                url = url[0:-2] + ("=s0" if containsS0 else "=s1600")
                return "https://2.bp.blogspot.com/" + url + sep + rest

            pages = [beau(match) for match in matches]
                    
            return render(request, 'comics/get_issue.html', {'issue': issue,
                                                            'pages': pages})
        except Exception as e:
            print(e)
            return render(request, './404error.html')
    else :
        return render(request, './404error.html')
    
def ajax_search(request):
    if 'term' in request.GET:
        series = Series.objects.filter(cleanname__istartswith = request.GET.get('term'))[:10]
        results = [{"name":"{} {}".format(s.cleanname, s.publicationdate),
                    "series_id":s.series_id} for s in series]
        return JsonResponse(results, safe=False)