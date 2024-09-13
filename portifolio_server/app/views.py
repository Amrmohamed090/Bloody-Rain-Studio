from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import BackgroundVideo, WebsiteText, Service, Image, Project, Visitor, ProjectVisit, NewsletterSubscriber, Post 
from django.core.mail import send_mail
from .forms import ContactForm, NewsletterForm
from django.utils import timezone
from django.contrib.gis.geoip2 import GeoIP2  # For geolocation
from django.contrib.admin import AdminSite
from django.utils import timezone
from django.db.models import Max
from .forms import ContactForm
from django.contrib import messages
from django.urls import reverse
from django.views.generic import View


def register_new_visitor(request, active_project=None):
    visitor_ip = get_client_ip(request)
    visitor_location = get_visitor_location(visitor_ip)
    
    # Find the latest timestamp among all visitors with the same IP address
    latest_visitor = Visitor.objects.filter(ip_address=visitor_ip).order_by('-timestamp').first()

    # Create a new visitor if there are no existing visitors with the same IP address
    if latest_visitor is None or (timezone.now() - latest_visitor.timestamp).total_seconds() > 300:
        current_visitor = Visitor.objects.create(ip_address=visitor_ip, location=visitor_location)
    else:
        current_visitor = latest_visitor

    if active_project:
        # Check if the visitor has already visited this project
        project_visit_exists = ProjectVisit.objects.filter(visitor=current_visitor, project=active_project).order_by('-timestamp').first()
        if project_visit_exists is None or (timezone.now() - project_visit_exists.timestamp).total_seconds() > 300:
            # If the same visitor hasn't visited this project for 300 seconds, create a new project visit
            ProjectVisit.objects.create(visitor=current_visitor, project=Project.objects.get(pk=active_project))

def register_subscriber(email):
    if not NewsletterSubscriber.objects.filter(email=email).exists():
            # Email doesn't exist, create a new subscriber
            subscriber = NewsletterSubscriber(email=email)
            subscriber.save()

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print("form valid")
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            subscribe_newsletter = form.cleaned_data['subscribe_newsletter']

            # Handle subscription logic if needed
            if subscribe_newsletter:
                print("Handling subscription logic...")
                register_subscriber(email)

            # Attempt to send email
            try:
                send_mail(
                    subject=subject,
                    message=f'Name: {full_name}\nEmail: {email}\n\nMessage: {message}',
                    from_email=None,  # Use default sender
                    recipient_list=['contact@bloodyrainstudios.com', email],  # Replace with your email
                )

                # Flag indicating successful message submission
                request.session['message_sent'] = True
                
                messages.success(request, 'Your message has been sent successfully!')
                print("email valid")
                return HttpResponseRedirect(reverse('app-home') + '#contact_us')

            except Exception as e:
                # Flag indicating message submission error
                print("email invalid")
                request.session['message_error'] = True
                print(e)
                return HttpResponseRedirect(reverse('app-home') + '#contact_us')

        else:
            print("invalid form")
            for field, error in form.errors.items():
                # Flag indicating message submission error
                request.session['message_error'] = True
                print(field,error)
            return HttpResponseRedirect(reverse('app-home') + '#contact_us')

    else:
        form = ContactForm()

    return render(request, 'app/index.html', {'form': form})

def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            register_subscriber(email)
            return HttpResponseRedirect(reverse('app-home'))  # Redirect to home page after subscription

    else:
        form = NewsletterForm()



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
    register_new_visitor(request, active_project=None)

    main_video = BackgroundVideo.objects.filter(is_main=True).first()
    text = WebsiteText.objects.filter(is_main=True).first()
    
    services = Service.objects.all()
    
    
    context = {
        'main_video': main_video,
        'services': services,
        'text': text,
        }
    if request.session.get('cookies_accepted'):
        context['cookies_accepted'] = True
    return render(request, 'app/index.html', context)

def portfolio(request, navbar_active):
    register_new_visitor(request, active_project=None)


    pagename = request.GET.get('pageid')  # Get the value of pagename from query parameters
    projects = Project.objects.all()
    services = Service.objects.all()
    
    context = {
        'pagename': pagename,
        'projects': projects,
        'services': services,
        'navbar_active': navbar_active,

    }
    
    return render(request, 'app/portfolio.html', context)


def project(request, active):
    register_new_visitor(request, active_project=active)

    active_project = get_object_or_404(Project, pk=active)



    return render(request, 'app/project.html', {'active_project': active_project})


def careers(request):
    register_new_visitor(request)

    context = {}


    return render(request, 'app/careers.html', context)


def blog(request):
    register_new_visitor(request)

    
    posts = Post.objects.all()
    context = {'posts': posts}

    return render(request, 'app/blog.html', context)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'app/post_page.html', {'post': post})



def privacy(request):
    register_new_visitor(request)

    context = {}


    return render(request, 'app/privacy.html', context)


class RobotsTextView(View):
    content = """User-agent: *
    Disallow: /admin/
    Disallow: /login/
    """

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.content, content_type='text/plain')