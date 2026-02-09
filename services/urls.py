from django.urls import path

from . import views

urlpatterns = [
    path("", views.service_list, name="service_list"),
    path("staff/services/", views.service_admin_list, name="service_admin_list"),
    path("staff/services/new/", views.service_create, name="service_create"),
    path("staff/services/<int:pk>/edit/", views.service_update, name="service_update"),
    path("staff/services/<int:pk>/delete/", views.service_delete, name="service_delete"),
    path("staff/slots/bulk/", views.slot_bulk_create, name="slot_bulk_create"),
    path("staff/slots/bulk/success/", views.slot_bulk_create_success, name="slot_bulk_create_success"),
]
