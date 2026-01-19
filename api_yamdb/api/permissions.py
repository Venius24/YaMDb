from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Читать могут все, создавать — только авторизованные
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        # Просмотр разрешен всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Редактирование и удаление — только автору
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем, а редактирование (категории, жанры) только админу.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            (request.user.is_authenticated and request.user.is_admin)
        )


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """
    Для отзывов и комментариев:
    - Читать может любой (ReadOnly).
    - Создавать — любой авторизованный.
    - Редактировать/Удалять — автор, модератор или админ.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (
            obj.author == request.user or
            request.user.is_moderator or
            request.user.is_admin
        )
    

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем, а редактирование только сотрудникам (staff).
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_moderator or request.user.is_admin
            or request.user.is_staff
        )