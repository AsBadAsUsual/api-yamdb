from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Пермишн даёт доступ не для чтения только админу"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrModeratorOrAuthor(BasePermission):
    """Пермишн даёт доступ не для чтения автору, модератору и админу"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdmin(BasePermission):
    """Пермишн даёт доступ только админу"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
