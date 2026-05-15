from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Lead
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'landing/index.html')

def privacy(request):
    return render(request, 'landing/privacy.html')

def terms(request):
    return render(request, 'landing/terms.html')

def success(request):
    # Simple security check: redirect to home if the verification token is missing
    # This prevents users from just typing /success/ to get the download link
    verify = request.GET.get('v')
    if verify != 'mc_launch_2024':
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
