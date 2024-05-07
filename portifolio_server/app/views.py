from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import BackgroundVideo, Service, Image, Project
from django.core.mail import send_mail
from .forms import ContactForm

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



    

def home(request):
    main_video = BackgroundVideo.objects.filter(is_main=True).first()
    services = Service.objects.all()

    context = {
        'main_video': main_video,
        'services': services
    }

   
    
   

    
    return render(request, 'app/index.html', context)
# Create your views here.


def portfolio(request):
    pagename = request.GET.get('pagename')  # Get the value of pagename from query parameters
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