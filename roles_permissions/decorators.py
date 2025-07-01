from django.http import HttpResponseForbidden
from functools import wraps
from .services import verifierPermission

def permission_requise(permission_code):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentification requise")
            if verifierPermission(request.user.id, permission_code):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Permission refusée")
        return _wrapped_view
    return decorator
