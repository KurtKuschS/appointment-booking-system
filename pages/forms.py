import re
from urllib.parse import urlparse

from django import forms
from django.core.validators import URLValidator

from .models import AboutPage, AboutPhoto, ContactPage, GalleryPage, GalleryPhoto, PolicyPage


class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = ("title", "story", "experience", "certifications")
        widgets = {
            "story": forms.Textarea(attrs={"rows": 5}),
            "experience": forms.Textarea(attrs={"rows": 5}),
            "certifications": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "input"})


class AboutPhotoForm(forms.ModelForm):
    class Meta:
        model = AboutPhoto
        fields = ("image", "caption", "order")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "input"})

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image
        _validate_image_upload(image)
        return image


class GalleryPageForm(forms.ModelForm):
    class Meta:
        model = GalleryPage
        fields = ("title", "subtitle")
        widgets = {
            "subtitle": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "input"})


class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ("before_image", "after_image", "caption", "order")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "input"})
        self.fields["order"].required = False
        self.fields["before_image"].required = False

    def clean(self):
        cleaned = super().clean()
        before_image = cleaned.get("before_image")
        after_image = cleaned.get("after_image")
        caption = cleaned.get("caption")

        has_before = bool(before_image) or bool(getattr(self.instance, "before_image", None))
        has_other_data = any([after_image, caption]) or bool(self.files)

        if has_other_data and not has_before:
            self.add_error("before_image", "Este campo es obligatorio.")

        return cleaned

    def clean_before_image(self):
        image = self.cleaned_data.get("before_image")
        if not image:
            return image
        _validate_image_upload(image)
        return image

    def clean_after_image(self):
        image = self.cleaned_data.get("after_image")
        if not image:
            return image
        _validate_image_upload(image)
        return image


class ContactPageForm(forms.ModelForm):
    map_embed_url = forms.CharField(required=False)

    class Meta:
        model = ContactPage
        fields = ("title", "address", "schedule", "phone", "whatsapp", "email", "map_embed_url")
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "schedule": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "input"})

    def clean_map_embed_url(self):
        value = self.cleaned_data.get("map_embed_url", "")
        if not value:
            return value

        value = value.strip()

        if "<iframe" in value:
            match = re.search(r'src=["\"]([^"\"]+)["\"]', value)
            if not match:
                raise forms.ValidationError("No se encontro el src del iframe.")
            value = match.group(1)

        validator = URLValidator(schemes=["https"])
        try:
            validator(value)
        except forms.ValidationError as exc:
            raise forms.ValidationError("El enlace de mapa no es valido.") from exc

        parsed = urlparse(value)
        allowed_hosts = {"www.google.com", "google.com", "maps.google.com"}
        if parsed.netloc not in allowed_hosts:
            raise forms.ValidationError("Solo se permite un enlace embed de Google Maps.")

        return value


def _validate_image_upload(image):
    allowed_types = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
    max_size = 5 * 1024 * 1024
    content_type = getattr(image, "content_type", "")

    if content_type not in allowed_types:
        raise forms.ValidationError("Formato de imagen no permitido.")
    if image.size > max_size:
        raise forms.ValidationError("La imagen supera el limite de 5MB.")


class PolicyPageForm(forms.ModelForm):
    class Meta:
        model = PolicyPage
        fields = ("title", "cancellation", "lateness", "before_after")
        widgets = {
            "cancellation": forms.Textarea(attrs={"rows": 4}),
            "lateness": forms.Textarea(attrs={"rows": 4}),
            "before_after": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({"class": "input"})
