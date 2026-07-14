from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import Lead
from django.views.decorators.csrf import csrf_exempt
import json

SUPPORTED_LANGUAGES = ("en", "ar", "fr")


def _pick_language_from_header(accept_language):
    for language_range in accept_language.split(","):
        code = language_range.split(";")[0].strip().lower().split("-")[0]
        if code in SUPPORTED_LANGUAGES and code != "en":
            return code
    return "en"

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /success/\n"
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}\n"
    )
    return HttpResponse(content, content_type="text/plain")

def google_verification(request):
    return HttpResponse("google-site-verification: google91f4a71bffa82687.html", content_type="text/html")

def sitemap_xml(request):
    # Hardcode HTTPS domain — app runs behind Coolify reverse proxy
    domain = 'https://monstercreative.lbahi.digital'
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url>\n    <loc>{domain}/</loc>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
        f'  <url>\n    <loc>{domain}/features/arabic-voiceover/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
        f'  <url>\n    <loc>{domain}/features/virtual-try-on/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
        f'  <url>\n    <loc>{domain}/features/image-resizer/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
        f'  <url>\n    <loc>{domain}/privacy/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.3</priority>\n  </url>\n'
        f'  <url>\n    <loc>{domain}/terms/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.3</priority>\n  </url>\n'
        '</urlset>'
    )
    return HttpResponse(content, content_type="application/xml")
def index(request, lang="en"):
    if lang not in SUPPORTED_LANGUAGES:
        lang = "en"

    context = {
        'FREEMIUS_PRODUCT_ID': settings.FREEMIUS_PRODUCT_ID,
        'FREEMIUS_PUBLIC_KEY': settings.FREEMIUS_PUBLIC_KEY,
        'FREEMIUS_PLAN_ID': settings.FREEMIUS_PLAN_ID,
        'LANGUAGE_CODE': lang,
        'LANGUAGE_DIR': 'rtl' if lang == 'ar' else 'ltr',
        'LANGUAGE_URLS': {
            'en': '/',
            'ar': '/ar/',
            'fr': '/fr/',
        },
        'CURRENT_LANGUAGE_URL': '/' if lang == 'en' else f'/{lang}/',
    }
    response = render(request, 'landing/index.html', context)
    response.set_cookie('site_language', lang, max_age=60 * 60 * 24 * 365, samesite='Lax')
    return response


def localized_index(request, lang):
    return index(request, lang=lang)


def language_redirect(request):
    saved_language = request.COOKIES.get("site_language")
    if saved_language == "en":
        return index(request)
    if saved_language in ("ar", "fr"):
        return redirect(f"/{saved_language}/")

    detected_language = _pick_language_from_header(request.META.get("HTTP_ACCEPT_LANGUAGE", ""))
    if detected_language in ("ar", "fr"):
        return redirect(f"/{detected_language}/")

    return index(request)

def arabic_voiceover(request):
    return render(request, 'landing/arabic_voiceover.html')

def virtual_try_on(request):
    return render(request, 'landing/virtual_try_on.html')

def image_resizer(request):
    return render(request, 'landing/image_resizer.html')

def privacy(request):
    return render(request, 'landing/privacy.html')

def terms(request):
    return render(request, 'landing/terms.html')

def success(request):
    # Simple security check: redirect to home if the verification token is missing
    # This prevents users from just typing /success/ to get the download link.
    # We also allow access if redirecting from Freemius (which appends plan_id / user_id / payment_id).
    verify = request.GET.get('v')
    from_freemius = any(k in request.GET for k in ['user_id', 'plan_id', 'payment_id', 'subscription_id'])
    
    if verify != 'mc_launch_2024' and not from_freemius:
        return redirect('index')
    return render(request, 'landing/success.html')

@csrf_exempt
def capture_lead(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            
            if name and email:
                lead = Lead.objects.create(name=name, email=email, phone=phone or "")
                return JsonResponse({'status': 'success', 'message': 'Lead captured successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Name and Email are required'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
