from django.core.exceptions import PermissionDenied
from apps.menu.models import Restaurant

def user_is_owner(function):
    def wrap(request, *args, **kwargs):
        entry = Restaurant.objects.get(id=kwargs['rest_id'])

        if entry.owner.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
