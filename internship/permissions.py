from rest_framework import permissions

class IsOwnerBusinessmanOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == "employer"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.employer == request.user


class IsStudentToApplyOrOwnerDelete(permissions.BasePermission):
    """
    - POST: только студент
    - DELETE: только студент, если он автор заявки
    - GET: студент видит только свои заявки, бизнесмен — только на свои стажировки (в view)
    """
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated and request.user.role == "student"
        if request.method == "DELETE":
            return request.user.is_authenticated and request.user.role == "student"
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.student == request.user
        return True
