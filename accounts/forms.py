from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import ClientProfile

User = get_user_model()


phone_validator = RegexValidator(
    regex=r"^\+?[0-9\s]{8,15}$",
    message="Usa solo numeros, espacios y un '+' opcional. Largo 8 a 15.",
)


class SignupForm(UserCreationForm):
    phone = forms.CharField(label="Telefono", max_length=20, validators=[phone_validator])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        autocomplete = {
            "username": "username",
            "first_name": "given-name",
            "last_name": "family-name",
            "email": "email",
            "phone": "tel",
            "password1": "new-password",
            "password2": "new-password",
        }
        for field_name in self.fields:
            attrs = {"class": "input"}
            if field_name in autocomplete:
                attrs["autocomplete"] = autocomplete[field_name]
            self.fields[field_name].widget.attrs.update(attrs)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        autocomplete = {
            "first_name": "given-name",
            "last_name": "family-name",
            "email": "email",
        }
        for field_name in self.fields:
            attrs = {"class": "input"}
            if field_name in autocomplete:
                attrs["autocomplete"] = autocomplete[field_name]
            self.fields[field_name].widget.attrs.update(attrs)


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ("phone",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "input", "autocomplete": "tel"})
        self.fields["phone"].validators.append(phone_validator)
