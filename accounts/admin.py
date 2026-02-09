from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import ClientProfile

User = get_user_model()


class ClientProfileInline(admin.TabularInline):
	model = ClientProfile
	extra = 0


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "phone")
	search_fields = ("user__username", "user__email", "phone")


# Unregister default User admin to attach profile inline.
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
	search_fields = ("username", "email", "first_name", "last_name")
	list_filter = ("is_staff", "is_active")
	inlines = [ClientProfileInline]
