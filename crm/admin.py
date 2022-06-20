from django.contrib import admin
from crm.models import Client, Event, Contract

class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "mobile",
        "company",
        # "company_is_customer",
        "sales_contact")
    list_filter = (
        "sales_contact",
        "last_name",
        "email",
        # "company__is_customer",
        "company")

class EventAdmin(admin.ModelAdmin):
    list_display = (
        # "contract",
        "date_created",
        "support_contact",
        "event_status",
        "attendees",
        "event_date")
    list_filter = (
        "support_contact",
        "event_status",
        "event_date")
        # "contract__client__last_name",
        # "contract__client__email")

class ContractAdmin(admin.ModelAdmin):
    readonly_fields=('status',)

    def get_form(self, request, obj=None, **kwargs):
        print(request.user)
        form = super().get_form(request, obj, **kwargs)
        return form
admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Contract, ContractAdmin)