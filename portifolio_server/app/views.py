from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import BackgroundVideo, Service, Image, Project, Visitor, ProjectVisit
from django.core.mail import send_mail
from .forms import ContactForm
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2  # For geolocation
from django.contrib.admin import AdminSite
from django.utils import timezone
from django.db.models import Max
from .forms import ContactForm
from django.contrib import messages
def register_new_visitor(request, active_project=None):
    visitor_ip = get_client_ip(request)
    visitor_location = get_visitor_location(visitor_ip)
    
    # Find the latest timestamp among all visitors with the same IP address
    latest_visitor = Visitor.objects.filter(ip_address=visitor_ip).order_by('-timestamp').first()

    # Create a new visitor if there are no existing visitors with the same IP address
    if latest_visitor is None or (timezone.now() - latest_visitor.timestamp).total_seconds() > 3600:
        current_visitor = Visitor.objects.create(ip_address=visitor_ip, location=visitor_location)
    else:
        current_visitor = latest_visitor

    if active_project:
        # Check if the visitor has already visited this project
        project_visit_exists = ProjectVisit.objects.filter(visitor=current_visitor, project=active_project).exists()
        
        if not project_visit_exists:
            # If the visitor hasn't visited this project, create a new project visit
            ProjectVisit.objects.create(visitor=current_visitor, project=Project.objects.get(pk=active_project))

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Attempt to send email
            try:
                send_mail(
                    subject='Contact Us Form Submission',
                    message=f'Name: {full_name}\nPhone: {phone_number}\nEmail: {email}\n\nMessage: {message}',
                    from_email=None,  # Use default sender
                    recipient_list=['amro.mohamed.023@gmail.com'],  # Replace with your email
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, f'Failed to send message: {str(e)}')
               
        else:
            for field, error in form.errors.items():
                messages.error(request, f'{field.capitalize()}: {error.as_text()}')
        
        return redirect('app-home')  # Redirect to the home page after form submission
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})


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

    

def home(request, message_contactus=None):

    register_new_visitor(request, active_project=None)


    main_video = BackgroundVideo.objects.filter(is_main=True).first()
    services = Service.objects.all()
    
    visitor_ip = get_client_ip(request)
    visitor_location = get_visitor_location(visitor_ip)

    

    register_new_visitor(request)

    context = {
        'main_video': main_video,
        'services': services,
        'message' : message_contactus

    }

    return render(request, 'app/index.html', context)


def portfolio(request):
    register_new_visitor(request, active_project=None)


    pagename = request.GET.get('pageid')  # Get the value of pagename from query parameters
    projects = Project.objects.all()
    services = Service.objects.all()
    
    context = {
        'pagename': pagename,
        'projects': projects,
        'services': services,

    }
    
    return render(request, 'app/portfolio.html', context)


def project(request, active):
    register_new_visitor(request, active_project=active)


    active_project = get_object_or_404(Project, pk=active)



    return render(request, 'app/project.html', {'active_project': active_project})
