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




admin.site.register(Visitor)

admin.site.register(ProjectVisit)

admin.site.register(BackgroundVideo)

admin.site.register(Service)



