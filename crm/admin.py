from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Q
from crm.models import Client, Event, Contract
from crm import permissions


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "sales_contact",
        "first_name",
        "last_name",
        "email",
        "phone",
        "mobile",
        "company",)

    list_filter = ("sales_contact",)

    def has_add_permission(self, request, obj=None):
        return permissions.permission(
            request.user, 'create', ['crm', 'client'])

    def has_change_permission(self, request, obj=None):
        return permissions.permission(
            request.user, 'update', ['crm', 'client'], obj)

    def has_delete_permission(self, request, obj=None):
        return permissions.permission(
            request.user, 'destroy', ['crm', 'client'], obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if (db_field.name == "sales_contact"
                and request.user.is_superuser is not True):
            kwargs["queryset"] = User.objects.filter(
                username=request.user.username)
        return super(ClientAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and request.user.is_superuser is not True:
            return self.readonly_fields + ("sales_contact",)
        return self.readonly_fields


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "date_created",
        "support_contact",
        "event_status",
        "attendees",
        "event_date")

    list_filter = (
        "support_contact",
        "event_status",
        "event_date")

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and request.user.is_superuser is not True:
            return self.readonly_fields + ("contract", "support_contact")
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser is not True:
            if db_field.name == "contract":
                kwargs["queryset"] = Contract.objects.filter(sales_contact=request.user).filter(Q(event__isnull=True))
            # if db_field.name == "support_contact":
            #     kwargs["queryset"] = User.objects.filter(username=request.user.username)
        return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request, obj=None):
        return permissions.permission(request.user, 'create', ['crm', 'event'])

    def has_change_permission(self, request, obj=None):
        return permissions.permission(request.user, 'update', ['crm', 'event'], obj)

    def has_delete_permission(self, request, obj=None):
        return permissions.permission(request.user, 'destroy', ['crm', 'event'])

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class ContractAdmin(admin.ModelAdmin):
    readonly_fields = ('status',)
    list_display = ('sales_contact', 'client', 'date_created')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def has_add_permission(self, request, obj=None):
        return permissions.permission(request.user, 'create', ['crm', 'contract'])

    def has_change_permission(self, request, obj=None):
        return permissions.permission(request.user, 'update', ['crm', 'contract'])

    def has_delete_permission(self, request, obj=None):
        return permissions.permission(request.user, 'destroy', ['crm', 'contract'])

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "sales_contact" and request.user.is_superuser is not True:
            kwargs["queryset"] = User.objects.filter(
                username=request.user.username)
        return super(ContractAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)
# admin.site.register(Event_Status)
