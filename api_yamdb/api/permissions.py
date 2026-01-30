from rest_framework.permissions import BasePermission, SAFE_METHODS, exceptions


class IsAdminOrReadOnly(BasePermission):
    """Пермишн даёт доступ не для чтения только админу"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated()
        return request.user.is_admin or request.user.is_staff
    

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