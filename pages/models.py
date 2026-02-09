from django.db import models


class AboutPage(models.Model):
    title = models.CharField(max_length=120, default="Sobre el salon")
    story = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class AboutPhoto(models.Model):
    page = models.ForeignKey(AboutPage, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="about")
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"Foto {self.order}"


class GalleryPage(models.Model):
    title = models.CharField(max_length=120, default="Galeria de trabajos")
    subtitle = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class GalleryPhoto(models.Model):
    page = models.ForeignKey(GalleryPage, related_name="photos", on_delete=models.CASCADE)
    before_image = models.ImageField(upload_to="gallery")
    after_image = models.ImageField(upload_to="gallery", blank=True)
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"Trabajo {self.order}"
