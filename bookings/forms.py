from django import forms
from django.utils import timezone

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["service", "slot"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.localdate()
        self.fields["slot"].queryset = (
            self.fields["slot"].queryset.filter(is_active=True, date__gte=today)
            .exclude(booking__isnull=False)
            .order_by("date", "start_time")
        )

    def clean_slot(self):
        slot = self.cleaned_data["slot"]
        if hasattr(slot, "booking"):
            raise forms.ValidationError("Este horario ya fue reservado.")
        return slot
