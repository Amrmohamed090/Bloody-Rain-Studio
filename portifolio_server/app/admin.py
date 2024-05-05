from django.contrib import admin

# Register your models here.
from .models import BackgroundVideo, Image, Service


admin.site.register(BackgroundVideo)

admin.site.register(Image)
admin.site.register(Service)