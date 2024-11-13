import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.hashers import make_password
from .models import UserActionLog

class ActionLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
     
        request.user_info = {
            'user': request.user if request.user.is_authenticated else None,
            'endpoint': request.path,
            'ip_address': request.META.get('REMOTE_ADDR'),
            'action_type': self.get_action_type(request.method),
        }
        
        request.user_info['data'] = self.get_filtered_data(request)

    def process_response(self, request, response):
        
        if hasattr(request, 'user_info'):
            status_code = response.status_code
            
            outcome = "PASS" if 200 <= status_code < 400 else "FAIL"
            
            
            UserActionLog.objects.create(
                user=request.user_info['user'],
                action_type=request.user_info['action_type'],
                endpoint=request.user_info['endpoint'],
                ip_address=request.user_info['ip_address'],
                status_code=status_code,
                outcome=outcome,
                details=f"Data: {request.user_info['data']}, Status: {status_code}"
            )
        return response

    def process_exception(self, request, exception):
        user = request.user if request.user.is_authenticated else None
        UserActionLog.objects.create(
            user=user,
            action_type='ERROR',
            endpoint=request.path,
            ip_address=request.META.get('REMOTE_ADDR'),
            status_code=500,
            outcome='FAIL',
            details=str(exception)
        )

    def get_action_type(self, method):
        return {
            'POST': 'CREATE',
            'PUT': 'UPDATE',
            'DELETE': 'DELETE',
            'GET': 'VIEW'
        }.get(method, 'OTHER')

    def get_filtered_data(self, request):
        if request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
               
                for key in ['password', 'password1', 'password2']:
                    if key in data:
                        data[key] = '***REDACTED***'
                return json.dumps(data)
            except json.JSONDecodeError:
                return "Invalid JSON"
        return "No data"