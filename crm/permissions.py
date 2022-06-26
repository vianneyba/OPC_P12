from rest_framework.permissions import BasePermission
from crm import models

def permission(user, action, module, obj=None):
    if user.is_superuser:
        return True
    elif action in ['list', 'retrieve']:
        return user.has_perm(f'{module[0]}.view_{module[1]}')
    elif action == 'create':
        return user.has_perm(f'{module[0]}.add_{module[1]}')
    elif action in ['update', 'partial_update']:
        if module[1] == 'event':
            if obj is not None and user == obj.support_contact and obj.event_status.pk == 1:
                return True
        elif module[1] == 'contract':
            if obj is not None and user == obj.sales_contact:
                return True
        elif module[1] == 'client':
            if obj is not None and user == obj.sales_contact:
                return True

        if obj is None:
            return user.has_perm(f'{module[0]}.change_{module[1]}')
    elif action == 'destroy':
        return user.has_perm(f'{module[0]}.delete_{module[1]}')

        
class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        return permission(request.user, view.action, ['auth', 'user'])


class ClientPermissions(BasePermission):
    def has_permission(self, request, view):
        return permission(request.user, view.action, ['crm', 'client'])

    def has_object_permission(self, request, view, obj):
        return permission(request.user, view.action, ['crm', 'client'], obj)


class ContractPermissions(BasePermission):
    def has_permission(self, request, view):
        return permission(request.user, view.action, ['crm', 'contract'])

    def has_object_permission(self, request, view, obj):
        return permission(request.user, view.action, ['crm', 'contract'], obj)


class EventPermission(BasePermission):
    def has_permission(self, request, view):
        return permission(request.user, view.action, ['crm', 'event'])

    def has_object_permission(self, request, view, obj):
        return permission(request.user, view.action, ['crm', 'event'], obj)

