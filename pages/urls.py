from django.urls import path

from . import views

urlpatterns = [
    path("about/edit/", views.about_edit, name="about_edit"),
    path("gallery/", views.gallery, name="gallery"),
    path("gallery/edit/", views.gallery_edit, name="gallery_edit"),
]
