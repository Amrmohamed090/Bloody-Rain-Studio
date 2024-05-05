from django.shortcuts import render
from django.http import HttpResponse
from .models import BackgroundVideo, Service, Image

def get_main_video():
    try:
        return BackgroundVideo.objects.get(is_main=True)
    except BackgroundVideo.DoesNotExist:
        # If no main video is set, return a default video or handle as per your requirement
        return None
    

def home(request):
    main_video = BackgroundVideo.objects.filter(is_main=True).first()
    services = Service.objects.all()


    context = {
        'main_video': main_video,
        'services': services
    }
    return render(request, 'app/index.html', context)
# Create your views here.


def portfolio(request, active):
    context = {
        'active': active,
    }
    return render(request, 'app/portfolio.html', context)

def project(request):
    
    
    return render(request, 'app/project.html')