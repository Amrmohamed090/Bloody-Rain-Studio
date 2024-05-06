from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

'''
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_images')
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"Image for {self.post.title}"

'''


class BackgroundVideo(models.Model):
    video = models.FileField(upload_to='background_videos/')
    is_main = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # If this video is marked as main, unmark all other videos
        if self.is_main:
            BackgroundVideo.objects.exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=100)
    
    description = models.TextField()
    home_page_services_section_images = models.ManyToManyField(Image, related_name='home_page_services')
    portfolio_page_service_images = models.ManyToManyField(Image, related_name='portfolio_page_services')

    def __str__(self):
        return self.title

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    project_images = models.ManyToManyField(Image)

    def __str__(self):
        return self.project_name
