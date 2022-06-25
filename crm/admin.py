from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from crm.models import Client, Event, Contract, Event_Status
from crm import permissions

class ClientAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return permissions.permission(request.user, 'create', ['crm', 'client'])

    def has_change_permission(self, request, obj=None):
        return permissions.permission(request.user, 'update', ['crm', 'client'], obj)

    def has_delete_permission(self, request, obj=None):
        return permissions.permission(request.user, 'destroy', ['crm', 'client'], obj)

    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "mobile",
        "company",
        "sales_contact")
    list_filter = (
        "sales_contact",
        "last_name",
        "email",
        "company")

class EventAdmin(admin.ModelAdmin):
    list_display = (
        "date_created",
        "support_contact",
        "event_status",
        "attendees",
        "event_date")

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser or request.user.groups.filter(name="sales_team").exists():
            return qs

        return qs.filter(support_contact=request.user)

    def has_add_permission(self, request, obj=None):
        return permissions.permission(request.user, 'create', ['crm', 'event'])

    def has_change_permission(self, request, obj=None):
        return permissions.permission(request.user, 'update', ['crm', 'event'])

    def has_delete_permission(self, request, obj=None):
        return permissions.permission(request.user, 'destroy', ['crm', 'event'])

    list_filter = (
        "support_contact",
        "event_status",
        "event_date")

class ContractAdmin(admin.ModelAdmin):
    readonly_fields=('status',)
    list_display = ('sales_contact', 'client' ,'date_created')

    def get_form(self, request, obj=None, **kwargs):
        print(request.user)
        form = super().get_form(request, obj, **kwargs)
        return form
    def has_add_permission(self, request, obj=None):
        return permissions.permission(request.user, 'create', ['crm', 'contract'])

    def has_change_permission(self, request, obj=None):
        return permissions.permission(request.user, 'update', ['crm', 'contract'])

    def has_delete_permission(self, request, obj=None):
        return permissions.permission(request.user, 'destroy', ['crm', 'contract'])

admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)
