from django.urls import path

from . import views

urlpatterns = [
    path("", views.service_list, name="service_list"),
    path("staff/services/", views.service_admin_list, name="service_admin_list"),
    path("staff/services/new/", views.service_create, name="service_create"),
    path("staff/services/<int:pk>/edit/", views.service_update, name="service_update"),
    path("staff/services/<int:pk>/delete/", views.service_delete, name="service_delete"),
    path("staff/slots/", views.slot_list, name="slot_list"),
    path("staff/slots/new/", views.slot_create, name="slot_create"),
    path("staff/slots/<int:pk>/edit/", views.slot_update, name="slot_update"),
    path("staff/slots/<int:pk>/delete/", views.slot_delete, name="slot_delete"),
    path("staff/slots/delete-unreserved/", views.slot_delete_unreserved, name="slot_delete_unreserved"),
    path("staff/slots/bulk/", views.slot_bulk_create, name="slot_bulk_create"),
    path("staff/slots/bulk/success/", views.slot_bulk_create_success, name="slot_bulk_create_success"),
]
