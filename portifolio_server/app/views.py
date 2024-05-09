from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import BackgroundVideo, Service, Image, Project, Visitor
from django.core.mail import send_mail
from .forms import ContactForm
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2  # For geolocation


def contact_us(request):

    ## handels the contact us
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                subject='Contact Us Form Submission',
                message=f'Name: {full_name}\nPhone: {phone_number}\nEmail: {email}\n\nMessage: {message}',
                from_email=None,  # Use default sender
                recipient_list=['your@email.com'],  # Replace with your email
            )
            return render(request, 'contact_success.html')  # Redirect to success page after sending email
        else:
            return render(request, 'contact_failed.html')
    else:
        form = ContactForm()



    return render(request, 'contact_form.html', {'form': form})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_visitor_location(ip_address):
    # Use GeoIP2 to get visitor's location based on their IP address
    g = GeoIP2()
    try:
        location = g.country(ip_address)
        visitor_location = f"{location['country_name']}"
    except:
        visitor_location = "Unknown"
    return visitor_location

    

def home(request):
    main_video = BackgroundVideo.objects.filter(is_main=True).first()
    services = Service.objects.all()

    # Get visitor's IP address
    visitor_ip = get_client_ip(request)

    # Get visitor's location based on IP address
    visitor_location = get_visitor_location(visitor_ip)

    # Save visitor's information to the database
    Visitor.objects.create(ip_address=visitor_ip, location=visitor_location)

    context = {
        'main_video': main_video,
        'services': services
    }

    return render(request, 'app/index.html', context)
# Create your views here.


def portfolio(request):
    pagename = request.GET.get('pageid')  # Get the value of pagename from query parameters
    print(pagename)
    projects = Project.objects.all()
    services = Service.objects.all()
    
    context = {
        'pagename': pagename,
        'projects': projects,
        'services': services
    }
    
    return render(request, 'app/portfolio.html', context)
def project(request, active):
     # Get the project object corresponding to the active parameter
    active_project = get_object_or_404(Project, pk=active)
    
    # Pass the active project to the template
    return render(request, 'app/project.html', {'active_project': active_project})