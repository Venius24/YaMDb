from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Полный доступ только для Администратора или Суперпользователя.
    Используется для эндпоинта /users/.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Чтение — всем.
    Создание и удаление — только Администратору.
    Используется для /categories/, /genres/ и /titles/.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            (request.user.is_authenticated and 
             (request.user.is_admin or request.user.is_superuser))
        )


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """
    Чтение — всем.
    Создание — любому авторизованному.
    Редактирование/Удаление — Автору, Модератору или Админу.
    Используется для /reviews/ и /comments/.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Сначала проверяем аутентификацию, чтобы не упасть на анониме
        if not request.user.is_authenticated:
            return False

        return (
            obj.author == request.user or
            request.user.is_moderator or
            request.user.is_admin or
            request.user.is_superuser
        )


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Чтение — всем.
    Создание — любому авторизованному.
    Редактирование/Удаление — Автору, Модератору или Админу.
    Используется для /reviews/ и /comments/.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Сначала проверяем аутентификацию, чтобы не упасть на анониме
        if not request.user.is_authenticated:
            return False

        return (
            request.user.is_moderator or
            request.user.is_admin or
            request.user.is_superuser
        )