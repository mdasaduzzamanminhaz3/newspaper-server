from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorEditorOrAdmin(BasePermission):

    def has_permission(self, request, view):

        # Allow everyone to read
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        # Only authenticated authors, editors and admins can write
        return (
            user
            and user.is_authenticated
            and user.role in ["author", "editor", "admin"]
        )

    def has_object_permission(self, request, view, obj):

        # Everyone can read accessible objects
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        # Editors and admins can manage all articles
        if user.role in ["editor", "admin"]:
            return True

        # Authors can manage their own articles
        return obj.author_id == user.id

class IsEditorOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        user = request.user

        return (
            user
            and user.is_authenticated
            and user.role in ["editor", "admin"]
        )


class IsCommentOwnerOrEditorAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role in ["editor", "admin"]:
            return True

        return obj.user_id == user.id
