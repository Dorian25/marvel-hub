from django.shortcuts import render
#from .models import Character

def home(request):
    return render(request, "characters/home.html", {})

#def details(request, pk):
#    character = Character.objects.get(id=pk)
#    return render(request, "characters/details.html", character) 
