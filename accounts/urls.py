from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile_edit, name="profile_edit"),
    path("staff/users/", views.user_list, name="user_list"),
]
