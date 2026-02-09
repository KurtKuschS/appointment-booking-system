from django.conf import settings
from django.db import models


class ClientProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20)
	notes = models.TextField(blank=True)

	def __str__(self) -> str:
		return f"{self.user.get_full_name() or self.user.username}"
