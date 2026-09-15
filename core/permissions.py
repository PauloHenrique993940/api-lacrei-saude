from rest_framework.permissions import BasePermission


class IsAuthenticatedWithAPIKey(BasePermission):
    message = "Autenticação necessária via API Key."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(
            request.auth is not None or (user is not None and getattr(user, "is_authenticated", False))
        )
