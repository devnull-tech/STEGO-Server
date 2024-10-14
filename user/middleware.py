from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import APIKey

class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin') or request.path == '/favicon.ico':
            return self.get_response(request)

        api_key = request.headers.get('API-KEY')
        if not api_key or not APIKey.objects.filter(key=api_key).exists():
            return JsonResponse({"error": "Invalid or missing API-KEY"}, status=403)

        return self.get_response(request)
