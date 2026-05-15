from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('api/lead/', views.capture_lead, name='capture_lead'),
    path('success/', views.success, name='success'),
]
