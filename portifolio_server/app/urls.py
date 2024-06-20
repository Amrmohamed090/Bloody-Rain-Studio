from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='app-home'),
    path('portfolio/', views.portfolio, name='app-portfolio'),
    path('portfolio/<str:navbar_active>/', views.portfolio, name='app-portfolio'),
    path('accept-cookies/', views.accept_cookies, name='accept_cookies'),
    path('decline-cookies/', views.decline_cookies, name='decline_cookies'),

    path('project/<int:active>/', views.project, name='app-project'),  
    path('contactus/', views.contact_us, name='app-contactus') , 
    path('newsletter/', views.newsletter, name='app-subscribeNewsletter')
]

