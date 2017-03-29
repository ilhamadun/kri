"""Participant decorators"""

from functools import wraps
from django.core.exceptions import PermissionDenied
from django.db import OperationalError


def has_access(division):
    """Check if user has an access to a division

    Raises:
        - PermissionDenied: user has no access

    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            try:
                if not request.user.university.has_access(division):
                    raise PermissionDenied
                return func(request, *args, **kwargs)
            except OperationalError:
                raise PermissionDenied
        return inner
    return decorator
