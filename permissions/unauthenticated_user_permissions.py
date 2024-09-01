from typing import Callable

from rest_framework.request import Request
from rest_framework.permissions import BasePermission


class WriteOnlyIfAuthenticated(BasePermission):
    """
    Allows read-only access to unauthenticated users
    and full access to authenticated users.
    """

    def has_permission(self, request: Request, view: Callable):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user and request.user.is_authenticated
