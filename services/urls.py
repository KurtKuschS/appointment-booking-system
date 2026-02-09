from django.urls import path

from . import views

urlpatterns = [
    path("", views.service_list, name="service_list"),
    path("staff/slots/bulk/", views.slot_bulk_create, name="slot_bulk_create"),
    path("staff/slots/bulk/success/", views.slot_bulk_create_success, name="slot_bulk_create_success"),
]
