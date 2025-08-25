from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def role_required(*allowed_roles: str):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if request.user.role in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Недостаточно прав")

        return _wrapped

    return decorator

