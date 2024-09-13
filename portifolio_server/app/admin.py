from django.core.mail import send_mail
from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from .models import BackgroundVideo, Image, Service, Project, Visitor, ProjectVisit, Newsletter, NewsletterSubscriber, WebsiteText

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.encoding import force_str
from bs4 import BeautifulSoup
from django.contrib.sites.models import Site
from orderable.admin import OrderableAdmin, OrderableTabularInline
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_image']
    ordering = ['name']  # This will sort the images alphabetically by name

    def display_image(self, obj):
        return format_html('<img src="{}" style="max-width:400px; max-height:400px;" />', obj.thumbnail.url)

    display_image.allow_tags = True
    display_image.short_description = 'Image Preview'



class ProjectAdmin(OrderableAdmin):
    list_display = ['project_name', 'display_thumbnail', 'project_description', 'sort_order_display']

    def display_thumbnail(self, obj):
        if obj.project_thumbnail:
            return format_html('<img src="{}" style="max-width:250px; max-height:250px;" />', obj.project_thumbnail.thumbnail.url)
        else:
            return "No Thumbnail"
    

    display_thumbnail.allow_tags = True
    display_thumbnail.short_description = 'Thumbnail'
    

    def __str__(self):
        return self.sort_order  

admin.site.register(Project , ProjectAdmin)


admin.site.register(Visitor)


admin.site.register(ProjectVisit)

admin.site.register(BackgroundVideo)

class ServiceAdmin(OrderableAdmin):
    list_display = ['title', 'description', 'sort_order_display']

    def __str__(self):
        return self.sort_order  



admin.site.register(Service, ServiceAdmin)



admin.site.register(NewsletterSubscriber)
admin.site.register(WebsiteText)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        newsletter = queryset.first()  # Assuming you only allow sending one newsletter at a time
        subscribers = NewsletterSubscriber.objects.filter(subscribed=True)

        # Get the current site to build absolute URLs
        current_site = Site.objects.get_current()
        print(current_site, "curr")
        site_url = f"https://mysite-k3q7.onrender.com"

        # Parse HTML content to update image URLs
        soup = BeautifulSoup(newsletter.body, 'html.parser')
        for img in soup.find_all('img'):
            src = img['src']
            if src.startswith('/'):
                img['src'] = f"{site_url}{src}"

        updated_html_content = str(soup)
        text_content = strip_tags(updated_html_content)  # Generate a plain text version of the HTML

        for subscriber in subscribers:
            subject = newsletter.subject

            # Create the email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=None,  # Use default sender
                to=[subscriber.email]
            )
            email.attach_alternative(updated_html_content, "text/html")

            # Send the email
            email.send(fail_silently=False)

        self.message_user(request, "Newsletter sent successfully.")

admin.site.register(Newsletter, NewsletterAdmin)


from django_summernote.admin import SummernoteModelAdmin
from .models import Post

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)