from django.shortcuts import render
from django.http import HttpResponse
from .models import BackgroundVideo

def get_main_video():
    try:
        return BackgroundVideo.objects.get(is_main=True)
    except BackgroundVideo.DoesNotExist:
        # If no main video is set, return a default video or handle as per your requirement
        return None
    

def home(request):
    main_video = BackgroundVideo.objects.filter(is_main=True).first()


    context = {
        'main_video': main_video,

    }
    return render(request, 'app/index.html', context)
# Create your views here.


def portfolio(request):
    return render(request, 'app/portfolio.html')