import time
from django.utils import timezone

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = int((time.time() - start_time) * 1000)
        
        # Log request
        print(f"{request.method} {request.path} -> {response.status_code} ({duration}ms)")
        
        # Add response header
        response['X-Response-Time'] = f"{duration}ms"
        return response