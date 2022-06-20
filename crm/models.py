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


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        User,
        related_name="contracts",
        on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateField()


class Event_Status(models.Model):
    status = models.BooleanField(default=False)


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
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, blank=True, null=True)
