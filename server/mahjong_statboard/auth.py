from rest_framework import permissions

from mahjong_statboard import models


class IsInstanceAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        instance_pk = view.kwargs.get('instance_pk')
        if not instance_pk:
            return False
        return request.user.is_superuser or request.user in models.Instance.objects.get(pk=instance_pk).admins.all()
