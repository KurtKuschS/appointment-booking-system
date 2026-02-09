from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from .forms import ClientProfileForm, SignupForm, UserProfileForm
from .models import ClientProfile

User = get_user_model()


def signup(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			ClientProfile.objects.create(user=user, phone=form.cleaned_data["phone"])
			login(request, user)
			return redirect("service_list")
	else:
		form = SignupForm()

	return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile_edit(request):
	profile, _ = ClientProfile.objects.get_or_create(user=request.user)

	if request.method == "POST":
		user_form = UserProfileForm(request.POST, instance=request.user)
		profile_form = ClientProfileForm(request.POST, instance=profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			return redirect("profile_edit")
	else:
		user_form = UserProfileForm(instance=request.user)
		profile_form = ClientProfileForm(instance=profile)

	context = {"user_form": user_form, "profile_form": profile_form}
	return render(request, "accounts/profile_edit.html", context)


def _is_staff(user):
	return user.is_staff


@user_passes_test(_is_staff)
def user_list(request):
	users = (
		User.objects.filter(is_staff=False)
		.select_related("clientprofile")
		.order_by("username")
	)
	return render(request, "accounts/user_list.html", {"users": users})
