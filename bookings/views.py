from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.db.models.functions import ExtractHour
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BookingCreateForm, BookingFilterForm
from .models import Booking
from services.models import AvailabilitySlot


@login_required
def booking_create(request):
	selected_service = request.POST.get("service") or request.GET.get("service")
	selected_date_str = request.POST.get("date") or request.GET.get("date")
	selected_date = None
	if selected_date_str:
		try:
			selected_date = date.fromisoformat(selected_date_str)
		except ValueError:
			selected_date = None
	if selected_date and selected_date < timezone.localdate():
		messages.error(request, "No puedes reservar en una fecha pasada.")
		selected_date = None
		selected_date_str = None

	filter_form = BookingFilterForm(
		request.GET or None,
		initial={"service": selected_service, "date": selected_date_str},
	)

	slots_queryset = AvailabilitySlot.objects.none()
	if selected_date:
		slots_queryset = (
			AvailabilitySlot.objects.filter(
				is_active=True,
				date=selected_date,
				date__gte=timezone.localdate(),
			)
			.exclude(booking__isnull=False)
			.order_by("start_time")
		)

	if request.method == "POST":
		booking_form = BookingCreateForm(request.POST, slot_queryset=slots_queryset)
		if booking_form.is_valid():
			booking = booking_form.save(commit=False)
			booking.client = request.user
			booking.save()
			messages.success(request, "Reserva confirmada.")
			return redirect("booking_list")
	else:
		booking_form = BookingCreateForm(
			initial={"service": selected_service},
			slot_queryset=slots_queryset,
		)

	context = {
		"filter_form": filter_form,
		"booking_form": booking_form,
		"selected_date": selected_date_str,
		"slots": list(slots_queryset),
	}
	return render(request, "bookings/booking_form.html", context)


@login_required
def booking_list(request):
	bookings = Booking.objects.filter(client=request.user).select_related("service", "slot")
	return render(request, "bookings/booking_list.html", {"bookings": bookings})


@login_required
@require_POST
def booking_cancel(request, pk):
	booking = get_object_or_404(Booking, pk=pk, client=request.user)
	if booking.status not in [Booking.STATUS_CANCELLED, Booking.STATUS_COMPLETED]:
		booking.status = Booking.STATUS_CANCELLED
		booking.save(update_fields=["status"])
	return redirect("booking_list")


def _is_staff(user):
	return user.is_staff


@login_required
@user_passes_test(_is_staff)
def admin_booking_list(request):
	bookings = Booking.objects.select_related("client", "service", "slot").order_by("-created_at")
	context = {
		"bookings": bookings,
		"status_choices": Booking.STATUS_CHOICES,
	}
	return render(request, "bookings/admin_booking_list.html", context)


@login_required
@user_passes_test(_is_staff)
@require_POST
def admin_booking_update_status(request, pk):
	booking = get_object_or_404(Booking, pk=pk)
	status = request.POST.get("status")
	valid = {choice[0] for choice in Booking.STATUS_CHOICES}
	if status in valid:
		booking.status = status
		booking.save(update_fields=["status"])
	return redirect("admin_booking_list")


@login_required
@user_passes_test(_is_staff)
def admin_dashboard(request):
	today = timezone.localdate()
	now_time = timezone.localtime().time()
	month_bookings = Booking.objects.filter(
		status=Booking.STATUS_COMPLETED,
		slot__date__year=today.year,
		slot__date__month=today.month,
	)
	income_total = month_bookings.aggregate(total=Sum("service__price"))["total"] or 0

	month_total = Booking.objects.filter(slot__date__year=today.year, slot__date__month=today.month).count()
	month_cancelled = Booking.objects.filter(
		status=Booking.STATUS_CANCELLED,
		slot__date__year=today.year,
		slot__date__month=today.month,
	).count()
	cancellation_rate = round((month_cancelled / month_total) * 100, 1) if month_total else 0

	today_total = Booking.objects.filter(slot__date=today).count()
	today_upcoming = Booking.objects.filter(
		slot__date=today,
		status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED],
		slot__start_time__gte=now_time,
	).count()

	top_services = (
		Booking.objects.filter(status=Booking.STATUS_COMPLETED)
		.values("service__name")
		.annotate(total=Count("id"))
		.order_by("-total")[:5]
	)

	top_clients = (
		Booking.objects.filter(status=Booking.STATUS_COMPLETED)
		.values("client__username", "client__first_name", "client__last_name")
		.annotate(total=Count("id"))
		.order_by("-total")[:5]
	)

	top_hours = (
		Booking.objects.filter(status__in=[Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED])
		.annotate(hour=ExtractHour("slot__start_time"))
		.values("hour")
		.annotate(total=Count("id"))
		.order_by("-total")[:5]
	)

	context = {
		"income_total": income_total,
		"top_services": top_services,
		"top_clients": top_clients,
		"month_label": today.strftime("%m/%Y"),
		"month_total": month_total,
		"month_cancelled": month_cancelled,
		"cancellation_rate": cancellation_rate,
		"today_total": today_total,
		"today_upcoming": today_upcoming,
		"top_hours": top_hours,
	}
	return render(request, "bookings/admin_dashboard.html", context)
