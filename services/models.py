from django.db import models


class Service(models.Model):
	name = models.CharField(max_length=100)
	duration_minutes = models.PositiveSmallIntegerField()
	price = models.DecimalField(max_digits=8, decimal_places=2)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name


class AvailabilitySlot(models.Model):
	date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ["date", "start_time"]
		constraints = [
			models.UniqueConstraint(
				fields=["date", "start_time", "end_time"],
				name="unique_slot_time_range",
			)
		]

	def __str__(self) -> str:
		return f"{self.date} {self.start_time}-{self.end_time}"
