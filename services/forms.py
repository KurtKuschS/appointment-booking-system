from django import forms
from django.utils import timezone

from .models import Service


class BulkSlotForm(forms.Form):
    WEEKDAY_CHOICES = [
        (0, "Lun"),
        (1, "Mar"),
        (2, "Mie"),
        (3, "Jue"),
        (4, "Vie"),
        (5, "Sab"),
        (6, "Dom"),
    ]

    start_date = forms.DateField(
        label="Fecha inicio",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        label="Fecha termino",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    start_time = forms.TimeField(
        label="Hora inicio",
        widget=forms.TimeInput(attrs={"type": "time"}),
    )
    end_time = forms.TimeField(
        label="Hora termino",
        widget=forms.TimeInput(attrs={"type": "time"}),
    )
    slot_minutes = forms.IntegerField(label="Duracion por bloque (min)", min_value=15, max_value=240)
    weekdays = forms.MultipleChoiceField(
        label="Dias",
        choices=WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    def clean(self):
        cleaned = super().clean()
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        start_time = cleaned.get("start_time")
        end_time = cleaned.get("end_time")
        slot_minutes = cleaned.get("slot_minutes")

        if start_date and end_date and start_date > end_date:
            self.add_error("end_date", "La fecha termino debe ser igual o posterior a inicio.")

        if start_time and end_time and start_time >= end_time:
            self.add_error("end_time", "La hora termino debe ser mayor que la hora inicio.")

        if slot_minutes and slot_minutes % 5 != 0:
            self.add_error("slot_minutes", "La duracion debe ser multiplo de 5.")

        if start_date and start_date < timezone.localdate():
            self.add_error("start_date", "La fecha inicio no puede ser en el pasado.")

        weekdays = cleaned.get("weekdays")
        if weekdays:
            cleaned["weekdays"] = [int(value) for value in weekdays]

        return cleaned


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("name", "description", "duration_minutes", "price", "is_active")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "input"})
