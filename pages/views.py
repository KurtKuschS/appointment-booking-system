from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import logging

from django.db.models import Max
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render

from .forms import AboutPageForm, AboutPhotoForm, GalleryPageForm, GalleryPhotoForm
from .models import AboutPage, AboutPhoto, GalleryPage, GalleryPhoto

logger = logging.getLogger(__name__)


def _is_staff(user):
    return user.is_staff


@user_passes_test(_is_staff)
def about_edit(request):
    about_page, _ = AboutPage.objects.get_or_create(id=1)

    PhotoFormSet = inlineformset_factory(
        AboutPage,
        AboutPhoto,
        form=AboutPhotoForm,
        fields=("image", "caption", "order"),
        extra=1,
        can_delete=True,
    )

    if request.method == "POST":
        page_form = AboutPageForm(request.POST, instance=about_page)
        formset = PhotoFormSet(request.POST, request.FILES, instance=about_page)
        if page_form.is_valid() and formset.is_valid():
            page_form.save()
            formset.save()
            messages.success(request, "Contenido actualizado.")
            return redirect("about")
    else:
        page_form = AboutPageForm(instance=about_page)
        formset = PhotoFormSet(instance=about_page)

    context = {"page_form": page_form, "formset": formset}
    return render(request, "pages/about_edit.html", context)


def gallery(request):
    page = GalleryPage.objects.prefetch_related("photos").first()
    return render(request, "gallery.html", {"gallery": page})


@user_passes_test(_is_staff)
def gallery_edit(request):
    gallery_page, _ = GalleryPage.objects.get_or_create(id=1)

    PhotoFormSet = inlineformset_factory(
        GalleryPage,
        GalleryPhoto,
        form=GalleryPhotoForm,
        fields=("before_image", "after_image", "caption", "order"),
        extra=1,
        can_delete=True,
    )

    if request.method == "POST":
        page_form = GalleryPageForm(request.POST, instance=gallery_page)
        formset = PhotoFormSet(
            request.POST,
            request.FILES,
            instance=gallery_page,
            queryset=gallery_page.photos.all(),
        )
        if page_form.is_valid() and formset.is_valid():
            page_form.save()
            instances = formset.save(commit=False)
            max_order = (
                GalleryPhoto.objects.filter(page=gallery_page).aggregate(max_order=Max("order"))[
                    "max_order"
                ]
                or 0
            )
            for instance in instances:
                if not instance.order:
                    max_order += 1
                    instance.order = max_order
                instance.page = gallery_page
                instance.save()
            for deleted in formset.deleted_objects:
                deleted.delete()
            messages.success(request, "Galeria actualizada.")
            return redirect("gallery")
        logger.warning("Gallery edit validation failed: %s", page_form.errors)
        logger.warning("Gallery formset errors: %s", formset.errors)
    else:
        page_form = GalleryPageForm(instance=gallery_page)
        formset = PhotoFormSet(instance=gallery_page, queryset=gallery_page.photos.all())

    context = {"page_form": page_form, "formset": formset}
    return render(request, "pages/gallery_edit.html", context)
