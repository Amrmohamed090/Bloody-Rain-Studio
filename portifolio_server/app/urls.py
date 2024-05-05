from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('portfolio/<int:active>/', views.portfolio, name='app-portfolio'),
    path('project/', views.project, name='app-project'),
    
]