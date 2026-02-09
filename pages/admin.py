from django.contrib import admin

from .models import AboutPage, AboutPhoto, ContactPage, GalleryPage, GalleryPhoto, PolicyPage


class AboutPhotoInline(admin.TabularInline):
    model = AboutPhoto
    extra = 1


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    inlines = [AboutPhotoInline]


class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 1


@admin.register(GalleryPage)
class GalleryPageAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    inlines = [GalleryPhotoInline]


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")


@admin.register(PolicyPage)
class PolicyPageAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
