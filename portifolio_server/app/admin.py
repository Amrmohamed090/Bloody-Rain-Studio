from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.urls import path
from .models import Subscriber
from .forms import NewsletterForm
from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from .models import BackgroundVideo, Image, Service, Project, Visitor, ProjectVisit
from django.views.decorators.cache import never_cache

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_image']

    def display_image(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px;" />', obj.image.url)

    display_image.allow_tags = True
    display_image.short_description = 'Image Preview'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'display_thumbnail', 'project_description']

    def display_thumbnail(self, obj):
        if obj.project_thumbnail:
            return format_html('<img src="{}" style="max-width:250px; max-height:250px;" />', obj.project_thumbnail.image.url)
        else:
            return "No Thumbnail"

    display_thumbnail.allow_tags = True
    display_thumbnail.short_description = 'Thumbnail'


from .forms import NewsletterForm

class NewsletterAdmin(admin.ModelAdmin):
    change_list_template = "admin/send_newsletter.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-newsletter/', self.admin_site.admin_view(self.send_newsletter))
        ]
        return custom_urls + urls

    def send_newsletter(self, request):
        if request.method == 'POST':
            form = NewsletterForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                recipients = [subscriber.email for subscriber in Subscriber.objects.all()]
                
                email = EmailMessage(subject, message, 'your-email@example.com', recipients)
                email.content_subtype = 'html'  # Set email content to HTML
                email.send()

                self.message_user(request, "Newsletter sent successfully")
                return redirect('..')
        else:
            form = NewsletterForm()
        return render(request, 'admin/send_newsletter.html', {'form': form})

admin.site.register(Subscriber, NewsletterAdmin)


admin.site.register(Visitor)

admin.site.register(ProjectVisit)

admin.site.register(BackgroundVideo)

admin.site.register(Service)



