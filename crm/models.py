from datetime import date
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        User,
        related_name='clients',
        on_delete=models.PROTECT)
    prospect = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def set_prospect_to_true(self):
        self.prospect = True
        self.save()


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        User, related_name="contracts", on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateField()

    def __str__(self):
        creation_date = date.strftime(self.date_created, "%d/%m/%Y")
        return f"Contrat: {self.client} du {creation_date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.client.set_prospect_to_true()


class Event_Status(models.Model):
    status = models.BooleanField(default=False)

    def __str__(self):
        if self.status:
            return "The event is not over"
        else:
            return "The event is over"


class Event(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(
        User,
        related_name="events",
        blank=True,
        null=True,
        on_delete=models.PROTECT)
    event_status = models.ForeignKey(Event_Status, on_delete=models.PROTECT, default=0)
    attendees = models.PositiveIntegerField(null=True, blank=True)
    event_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        creation_date = date.strftime(self.date_created, "%d/%m/%Y")
        return f"Event: {self.client} du {creation_date} ({self.event_status})"
