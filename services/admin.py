from django.contrib import admin

from .models import AvailabilitySlot, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("name", "description_preview", "duration_minutes", "price", "is_active")
	list_filter = ("is_active",)
	search_fields = ("name",)

	def description_preview(self, obj):
		return (obj.description[:40] + "...") if obj.description and len(obj.description) > 40 else obj.description

	description_preview.short_description = "Descripcion"


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
	list_display = ("date", "start_time", "end_time", "is_active")
	list_filter = ("date", "is_active")
