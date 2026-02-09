import re

from django import forms

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

        if "<iframe" in value:
            match = re.search(r'src=["\"]([^"\"]+)["\"]', value)
            if not match:
                raise forms.ValidationError("No se encontro el src del iframe.")
            return match.group(1)

        return value


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
