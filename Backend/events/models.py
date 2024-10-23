from django.db import models
from django.conf import settings
from users.models import User
import uuid

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
        ]
        ordering = ['start_time']

    def __str__(self):
        return self.title

class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['capacity'])
        ]
        ordering = ['name']

    def __str__(self):
        return self.name

class EventVenue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_venues')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='venue_events')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'venue', 'date')
        indexes = [
            models.Index(fields=['event'],),
            models.Index(fields=['venue'],),
            models.Index(fields=['date'],)
        ]  
        ordering = ['date']

    def __str__(self):
        return f"{self.event.name} at {self.venue.name} on {self.date}"

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_attendee = models.OneToOneField('EventAttendee', on_delete=models.CASCADE, related_name='ticket')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['event_attendee'], name='idx_ticket_event_attendee'),
            models.Index(fields=['price'], name='idx_ticket_price'),
        ]

    def __str__(self):
        return f"{self.event.title} - ${self.price}"

class EventAttendee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_attendees')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    ticket = models.OneToOneField(Ticket, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user'],),
            models.Index(fields=['event'],),
            models.Index(fields=['status'],),
        ]
        unique_together = ('user', 'event')
        ordering = ['created_at']  

    def __str__(self):
        return f"{self.user} - {self.event.name} ({self.status})"

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'CC', 'Credit Card',
        PAYPAL = 'PP', 'PayPal',
        BANK_TRANSFER = 'BT', 'Bank Transfer'
        OTHER = 'OT', 'Other'
    
    class Status(models.TextChoices):
        PAID = 'Paid', 'Paid'
        PENDING = 'Pending', 'Pending'
        FAILED = 'Failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=2, choices=PaymentMethod.choices)
    status = models.CharField(max_length=10, choices=Status.choices)
    transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['ticket'],),
            models.Index(fields=['status'],),
            models.Index(fields=['transaction_id']),
        ]

    def __str__(self):
        return self.payment_method