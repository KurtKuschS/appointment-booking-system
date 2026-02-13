from django.conf import settings
from django.db import models

from services.models import AvailabilitySlot, Service


class Booking(models.Model):
	STATUS_PENDING = "pending"
	STATUS_CONFIRMED = "confirmed"
	STATUS_CANCELLED = "cancelled"
	STATUS_COMPLETED = "completed"

	STATUS_CHOICES = [
		(STATUS_PENDING, "Pendiente"),
		(STATUS_CONFIRMED, "Confirmada"),
		(STATUS_CANCELLED, "Cancelada"),
		(STATUS_COMPLETED, "Completada"),
	]

	client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	service = models.ForeignKey(Service, on_delete=models.PROTECT)
	slot = models.OneToOneField(AvailabilitySlot, on_delete=models.PROTECT)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]
		constraints = [
			models.UniqueConstraint(
				fields=["slot"],
				name="unique_booking_per_slot",
			),
		]

	def __str__(self) -> str:
		return f"{self.client} - {self.service} - {self.slot}"
