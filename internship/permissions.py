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
    - PUT/PATCH: студент может редактировать свою заявку, работодатель — заявки на свои стажировки
    - GET: студент видит только свои заявки, работодатель — заявки на свои стажировки (фильтрация в view)
    """

    def has_permission(self, request, view):
        # Создавать заявку может только студент
        if request.method == "POST":
            return request.user.is_authenticated and request.user.role == "student"

        # Удалять заявку может только студент
        if request.method == "DELETE":
            return request.user.is_authenticated and request.user.role == "student"
        
        if request.method in permissions.SAFE_METHODS and request.user.role == "teacher":
            return True

        # Для остальных методов (GET, PUT, PATCH) — просто проверим, что пользователь авторизован
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Удалить может только студент-владелец
        if request.method == "DELETE":
            return obj.student == request.user
        
        if request.method in permissions.SAFE_METHODS and request.user.role == "teacher":
            return True

        # Обновить (PUT/PATCH) может студент-владелец или работодатель, создавший стажировку
        if request.method in ["PUT", "PATCH"]:
            return (
                obj.student == request.user
                or (
                    request.user.role == "employer"
                    and obj.internship.employer == request.user
                )
            )

        # Остальные методы (GET, HEAD, OPTIONS) доступны, если пользователь авторизован
        return True
