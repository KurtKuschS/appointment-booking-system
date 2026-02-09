from django.contrib import admin

from .models import AvailabilitySlot, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("name", "duration_minutes", "price", "is_active")
	list_filter = ("is_active",)
	search_fields = ("name",)


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
	list_display = ("date", "start_time", "end_time", "is_active")
	list_filter = ("date", "is_active")
