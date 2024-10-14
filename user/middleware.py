from django.http import JsonResponse
from .models import APIKey

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            return self.get_response(request)

        api_key = request.headers.get('API-KEY')
        if not api_key or not APIKey.objects.filter(key=api_key).exists():
            return JsonResponse({"error": "Invalid or missing API-KEY"}, status=403)

        return self.get_response(request)
