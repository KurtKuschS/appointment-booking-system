from django import forms
from django.utils import timezone

from .models import Booking
from services.models import Service


class BookingFilterForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.filter(is_active=True))
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].widget.attrs.update({"class": "input"})
        self.fields["date"].widget.attrs.update({"class": "input"})


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["service", "slot"]

    def __init__(self, *args, **kwargs):
        slot_queryset = kwargs.pop("slot_queryset", None)
        super().__init__(*args, **kwargs)
        today = timezone.localdate()
        if slot_queryset is None:
            slot_queryset = (
                self.fields["slot"].queryset.filter(is_active=True, date__gte=today)
                .exclude(booking__isnull=False)
                .order_by("date", "start_time")
            )
        self.fields["slot"].queryset = slot_queryset
        self.fields["slot"].empty_label = "Selecciona un horario"
        self.fields["service"].widget = forms.HiddenInput()
        self.fields["slot"].widget = forms.RadioSelect()

    def clean_slot(self):
        slot = self.cleaned_data["slot"]
        if hasattr(slot, "booking"):
            raise forms.ValidationError("Este horario ya fue reservado.")
        return slot
