from django.shortcuts import render
from django.http import Http404
from .models import Series
from .models import Issue
from django.core.paginator import Paginator
from bs4 import BeautifulSoup
import requests
import re
import binascii

def home(request):
    return render(request, "comics/home.html", {})

def home_series(request):
    page = request.GET.get('page')
    all_series = Series.objects.all().order_by('series_id')
    paginator = Paginator(all_series, 10) # Show 25 series per page
    list_series = paginator.get_page(page)

    return render(request, 'comics/home.html', {"all_series": all_series,
                                                "list_series":list_series})

def get_series(request, pk):
    try:
        series = Series.objects.get(series_id=pk)
    except Series.DoesNotExist:
        return render(request, './404error.html')
    
    issues = Issue.objects.filter(series_id=pk)

    return render(request, 'comics/series.html', {"series": series,
                                                  "issues": issues})

def get_issue(request, pk):
    try:
        issue = Issue.objects.get(issue_id=pk)
    except Issue.DoesNotExist:
        return render(request, './404error.html')
    
    # get url_read
    url = issue.url_read

    if url != "NA":
        pages = []
        soup = BeautifulSoup(requests.get(url).text, "lxml")

        all_script = soup.find_all("script")
        all_script_txt = [script.text for script in all_script]
        valid_script = ""
        for script_txt in all_script_txt:
            if "lstImages.push" in script_txt:
                valid_script = script_txt
                break
        
        chapter_images_regex = r"lstImages\.push\([\"'](.*)[\"']\)"

        matches = re.findall(chapter_images_regex, valid_script)
        
        def beau(url):
            # url is crypted by a function in Scripts/rguard.min.js?v=1.2.9
            # https://github.com/Xonshiz/comic-dl/issues/299
            # https://github.com/Xonshiz/comic-dl/pull/344/files
            url = url.replace("_x236", "d")
            url = url.replace("_x945", "g")

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
        #pages = [imageUrl for imageUrl in matches]
                
        return render(request, 'comics/issue.html', {'issue': issue,
                                                    'pages': pages})
    else :
        return render(request, './404error.html')