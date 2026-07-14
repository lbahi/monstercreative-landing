from django.urls import path
from . import views

urlpatterns = [
    path('', views.language_redirect, name='index'),
    path('ar/', views.localized_index, {'lang': 'ar'}, name='index_ar'),
    path('fr/', views.localized_index, {'lang': 'fr'}, name='index_fr'),
    path('features/arabic-voiceover/', views.arabic_voiceover, name='arabic_voiceover'),
    path('features/virtual-try-on/', views.virtual_try_on, name='virtual_try_on'),
    path('features/image-resizer/', views.image_resizer, name='image_resizer'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('api/lead/', views.capture_lead, name='capture_lead'),
    path('success/', views.success, name='success'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('google91f4a71bffa82687.html', views.google_verification, name='google_verification'),
]
