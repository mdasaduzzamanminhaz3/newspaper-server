
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorEditorOrAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.role in ["author", "editor", "admin"]

    def has_object_permission(self, request, view, obj):

        # Anyone with access can read the object
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        # Editor and Admin can manage all articles
        if user.role in ["editor", "admin"]:
            return True

        # Author can manage only their own articles
        return obj.author_id == user.id
