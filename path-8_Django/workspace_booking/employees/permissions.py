from rest_framework import permissions


class IsViewer(permissions.BasePermission):
    """
    Permission для посетителя - только просмотр
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Посетитель может только просматривать
        return request.method in permissions.SAFE_METHODS


class IsKeeper(permissions.BasePermission):
    """
    Permission для смотрителя - просмотр и перемещение сотрудников
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Смотритель может обновлять только рабочее место
        if request.method in ["PATCH", "PUT"]:
            # Проверяем, что обновляются только разрешенные поля
            allowed_fields = {"workplace"}
            if hasattr(request, "data"):
                updating_fields = set(request.data.keys())
                return updating_fields.issubset(allowed_fields)
        return False


class IsAdmin(permissions.BasePermission):
    """
    Permission для администратора - полные права
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает полный доступ администраторам, остальным - только чтение
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff
