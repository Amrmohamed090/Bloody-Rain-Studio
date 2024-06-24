from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
from orderable.models import Orderable
from django.urls import reverse
from bs4 import BeautifulSoup 

class BackgroundVideo(models.Model):
    video = models.FileField(upload_to='background_videos/')
    is_main = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # If this video is marked as main, unmark all other videos
        if self.is_main:
            BackgroundVideo.objects.exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)



class Image(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    
    def save(self, *args, **kwargs):
        if not self.name and self.image:
            # If name is not provided and there's an image, set name to the filename
            filename = os.path.basename(self.image.name)
            name, _ = os.path.splitext(filename)
            self.name = name

        super().save(*args, **kwargs)

        # Convert image to JPEG
        convert_to_jpg = False
        if self.image:
            filename = os.path.basename(self.image.name)
            print(filename.split('.')[-1])
            if not filename.split('.')[-1] == 'jpg':
                convert_to_jpg = True
        
        if self.image and convert_to_jpg:
            print("Converting to JPEG")
            img = PILImage.open(self.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Save the converted image to a BytesIO object
            output = BytesIO()
            img.save(output, format='JPEG', quality=75)
            output.seek(0)

            # Change the image field value to be the new converted file
            self.image.save(os.path.splitext(self.image.name)[0] + '.jpg',
                            ContentFile(output.getvalue()), save=False)
            print("image converted and saved")
            super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Service(Orderable):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    services_images = models.ManyToManyField(Image)
    sort_order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Set sort_order to pk if it's not already set
        if not self.sort_order:
            self.sort_order = self.pk
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Project(Orderable):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    project_category = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name='main_projects', null=True)
    project_thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, related_name='as_thumbnail', null=True)
    project_video_youtube = models.CharField(max_length=600, null=True, blank=True, help_text="Go to the youtube video. and right-click on the YouTube video. then select 'Copy embed code'. \n Paste here")
    project_images = models.ManyToManyField(Image)
    sort_order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Set sort_order to pk if it's not already set
        if not self.sort_order:
            self.sort_order = self.pk

        # if self.project_video_youtube:
        #     # Use BeautifulSoup to parse the HTML and modify the iframe
        #     soup = BeautifulSoup(self.project_video_youtube, 'html.parser')
        #     iframe = soup.find('iframe')
        #     if iframe:
        #         # Remove width and height attributes
        #         if 'width' in iframe.attrs:
        #             del iframe['width']
        #         if 'height' in iframe.attrs:
        #             del iframe['height']
        #         # Adjust size by adding CSS classes or style attributes
        #         iframe['class'] = 'youtube-iframe'  # Add your custom class
        #         iframe['style'] = 'width: 100%; height: 100%;'  # Example of inline styles

                # Update project_video_youtube with modified HTML
                # self.project_video_youtube = str(soup)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.project_name
    def get_absolute_url(self):
        return reverse('app-project', args=[str(self.pk)])
    

class Visitor(models.Model):
    ip_address = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)  # Indexing timestamp field
    
class ProjectVisit(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)  # Indexing timestamp field



    

class Newsletter(models.Model):
    subject = models.CharField(
        _("Email Subject"), max_length=250,
        null=False, blank=False
    )
    body = RichTextUploadingField()    
    def __str__(self):
        return self.subject
    
class NewsletterSubscriber(models.Model):
    email = models.CharField(max_length=100)
    subscribed = models.BooleanField(default=True)
    def __str__(self):
        return self.email