from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Project
class StaticViewSitemap(Sitemap):
    def items(self):
        return ['app-home','app-portfolio']
    def location(self, item):
        return reverse(item)
    
class ProjectSitemap(Sitemap):
    def items(self):
        return Project.objects.all()