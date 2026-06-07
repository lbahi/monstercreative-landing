from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('api/lead/', views.capture_lead, name='capture_lead'),
    path('success/', views.success, name='success'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('google91f4a71bffa82687.html', views.google_verification, name='google_verification'),
]
