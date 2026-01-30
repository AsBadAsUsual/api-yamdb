from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Пермишн даёт доступ не для чтения только админу"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrModeratorOrAuthor(BasePermission):
    """Пермишн даёт доступ не для чтения автору, модератору и админу"""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdmin(BasePermission):
    """Пермишн даёт доступ только админу"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin
