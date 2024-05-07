from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('portfolio/', views.portfolio, name='app-portfolio'),
    path('project/<int:active>/', views.project, name='app-project'),
    path('contact/', views.contact_us, name='contact_us'),

    
]