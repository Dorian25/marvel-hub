from django.shortcuts import render

# Create your views here.
def start_hub(request):
    return render(request, 'hub/home.html', {})