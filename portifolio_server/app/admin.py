from django.contrib import admin

# Register your models here.
from .models import BackgroundVideo, Image, Service, Project, Visitor


admin.site.register(BackgroundVideo)

admin.site.register(Image)
admin.site.register(Service)
admin.site.register(Project)
admin.site.register(Visitor)


