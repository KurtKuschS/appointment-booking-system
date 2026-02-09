from django.urls import path

from . import views

urlpatterns = [
    path("bookings/", views.booking_list, name="booking_list"),
    path("bookings/new/", views.booking_create, name="booking_create"),
    path("bookings/<int:pk>/cancel/", views.booking_cancel, name="booking_cancel"),
    path("staff/bookings/", views.admin_booking_list, name="admin_booking_list"),
    path("staff/bookings/<int:pk>/status/", views.admin_booking_update_status, name="admin_booking_update_status"),
]
