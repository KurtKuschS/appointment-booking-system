from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking


@login_required
def booking_create(request):
	initial = {}
	service_id = request.GET.get("service")
	if service_id:
		initial["service"] = service_id

	if request.method == "POST":
		form = BookingForm(request.POST)
		if form.is_valid():
			booking = form.save(commit=False)
			booking.client = request.user
			booking.save()
			return redirect("booking_list")
	else:
		form = BookingForm(initial=initial)

	return render(request, "bookings/booking_form.html", {"form": form})


@login_required
def booking_list(request):
	bookings = Booking.objects.filter(client=request.user).select_related("service", "slot")
	return render(request, "bookings/booking_list.html", {"bookings": bookings})


@login_required
def booking_cancel(request, pk):
	booking = get_object_or_404(Booking, pk=pk, client=request.user)
	if booking.status not in [Booking.STATUS_CANCELLED, Booking.STATUS_COMPLETED]:
		booking.status = Booking.STATUS_CANCELLED
		booking.save(update_fields=["status"])
	return redirect("booking_list")


def _is_staff(user):
	return user.is_staff


@user_passes_test(_is_staff)
def admin_booking_list(request):
	bookings = Booking.objects.select_related("client", "service", "slot").order_by("-created_at")
	context = {
		"bookings": bookings,
		"status_choices": Booking.STATUS_CHOICES,
	}
	return render(request, "bookings/admin_booking_list.html", context)


@user_passes_test(_is_staff)
def admin_booking_update_status(request, pk):
	booking = get_object_or_404(Booking, pk=pk)
	if request.method == "POST":
		status = request.POST.get("status")
		valid = {choice[0] for choice in Booking.STATUS_CHOICES}
		if status in valid:
			booking.status = status
			booking.save(update_fields=["status"])
	return redirect("admin_booking_list")
