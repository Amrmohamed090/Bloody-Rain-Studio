from django.urls import path
from . import views
from django.contrib import admin
from .views import RobotsTextView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='app-home'),
    path('portfolio/', views.portfolio, name='app-portfolio'),
    path('portfolio/<str:navbar_active>/', views.portfolio, name='app-portfolio'),
    path('contactus/', views.contact_us, name='app-contactus') , 

    path('project/<int:active>/', views.project, name='app-project'),  
    path('careers/', views.careers, name='app-careers') , 
    path('blog/', views.blog, name='app-blog') , 
    path('privacy/', views.privacy, name='app-privacy') ,
    path('newsletter/', views.newsletter, name='app-subscribeNewsletter'),
    path('robots.txt', RobotsTextView.as_view(), name='robots'),

]

