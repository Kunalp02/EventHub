from django.contrib import admin
from .models import Event, Venue, EventVenue, Ticket, EventAttendee, Payment

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('start_time', 'end_time')
    ordering = ('start_time',)

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity', 'created_at', 'updated_at')
    search_fields = ('name', 'address')
    list_filter = ('capacity',)
    ordering = ('name',)

class EventVenueAdmin(admin.ModelAdmin):
    list_display = ('event', 'venue', 'date', 'created_at', 'updated_at')
    search_fields = ('event__title', 'venue__name')
    list_filter = ('date',)
    ordering = ('date',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('event_attendee', 'price', 'created_at', 'updated_at')
    search_fields = ('event_attendee__user__username', 'event_attendee__event__title')
    ordering = ('created_at',)

class EventAttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket', 'created_at', 'updated_at')
    search_fields = ('user__username', 'event__title')
    list_filter = ('event',)
    ordering = ('created_at',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'amount', 'payment_method', 'status', 'created_at', 'updated_at')
    search_fields = ('ticket__event_attendee__user__username', 'transaction_id')
    list_filter = ('status', 'payment_method')
    ordering = ('created_at',)

admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(EventVenue, EventVenueAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(EventAttendee, EventAttendeeAdmin)
admin.site.register(Payment, PaymentAdmin)
