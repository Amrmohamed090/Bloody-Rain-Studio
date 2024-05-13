from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

class BackgroundVideo(models.Model):
    video = models.FileField(upload_to='background_videos/')
    is_main = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # If this video is marked as main, unmark all other videos
        if self.is_main:
            BackgroundVideo.objects.exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)




class Image(models.Model):
    name = models.CharField(max_length=100,  null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    def save(self, *args, **kwargs):
        if not self.name and self.image:
            # If name is not provided and there's an image, set name to the filename
            filename = os.path.basename(self.image.name)
            name, _ = os.path.splitext(filename)
            self.name = name

        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    services_images = models.ManyToManyField(Image)

    def __str__(self):
        return self.title

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    project_category = models.ForeignKey(Service, on_delete=models.CASCADE, related_name ='main_projects', null=True)
    project_thumbnail = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='as_thumbnail', null=True)
    project_images = models.ManyToManyField(Image)


    def __str__(self):
        return self.project_name
    
class Visitor(models.Model):
    ip_address = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Visitor #{self.pk}: IP Address - {self.ip_address}, Location - {self.location}, Timestamp - {self.timestamp}"

class ProjectVisit(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Visitor #{self.visitor.pk}, Project - {self.project}, Timestamp - {self.timestamp}"
