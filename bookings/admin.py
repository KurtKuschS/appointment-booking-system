from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ("client", "service", "slot", "status", "created_at")
	list_filter = ("status", "service")
	search_fields = ("client__username", "client__email")
