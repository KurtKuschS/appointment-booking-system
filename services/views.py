from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AvailabilitySlotForm, BulkSlotForm, ServiceForm
from .models import AvailabilitySlot, Service


def service_list(request):
	services = Service.objects.filter(is_active=True).order_by("name")
	context = {"services": services}
	return render(request, "services/service_list.html", context)


def _is_staff(user):
	return user.is_staff


@user_passes_test(_is_staff)
def service_admin_list(request):
	services = Service.objects.all().order_by("name")
	return render(request, "services/service_admin_list.html", {"services": services})


@user_passes_test(_is_staff)
def service_create(request):
	if request.method == "POST":
		form = ServiceForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("service_admin_list")
	else:
		form = ServiceForm()

	return render(request, "services/service_form.html", {"form": form, "title": "Crear servicio"})


@user_passes_test(_is_staff)
def service_update(request, pk):
	service = get_object_or_404(Service, pk=pk)
	if request.method == "POST":
		form = ServiceForm(request.POST, instance=service)
		if form.is_valid():
			form.save()
			return redirect("service_admin_list")
	else:
		form = ServiceForm(instance=service)

	context = {"form": form, "title": "Editar servicio", "service": service}
	return render(request, "services/service_form.html", context)


@user_passes_test(_is_staff)
def service_delete(request, pk):
	service = get_object_or_404(Service, pk=pk)
	if request.method == "POST":
		service.delete()
		return redirect("service_admin_list")

	return render(request, "services/service_confirm_delete.html", {"service": service})


@user_passes_test(_is_staff)
def slot_bulk_create(request):
	created_count = 0
	if request.method == "POST":
		form = BulkSlotForm(request.POST)
		if form.is_valid():
			created_count = _create_slots_from_form(form.cleaned_data)
			return redirect("slot_bulk_create_success")
	else:
		form = BulkSlotForm()

	context = {"form": form, "created_count": created_count}
	return render(request, "services/slot_bulk_create.html", context)


@user_passes_test(_is_staff)
def slot_bulk_create_success(request):
	return render(request, "services/slot_bulk_success.html")


@user_passes_test(_is_staff)
def slot_list(request):
	date_filter = request.GET.get("date")
	active_filter = request.GET.get("active")

	slots = AvailabilitySlot.objects.all().order_by("date", "start_time")
	if date_filter:
		slots = slots.filter(date=date_filter)
	if active_filter in ["0", "1"]:
		slots = slots.filter(is_active=active_filter == "1")

	context = {
		"slots": slots,
		"date_filter": date_filter,
		"active_filter": active_filter,
	}
	return render(request, "services/slot_list.html", context)


@user_passes_test(_is_staff)
def slot_create(request):
	if request.method == "POST":
		form = AvailabilitySlotForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("slot_list")
	else:
		form = AvailabilitySlotForm()

	return render(request, "services/slot_form.html", {"form": form, "title": "Crear horario"})


@user_passes_test(_is_staff)
def slot_update(request, pk):
	slot = get_object_or_404(AvailabilitySlot, pk=pk)
	if request.method == "POST":
		form = AvailabilitySlotForm(request.POST, instance=slot)
		if form.is_valid():
			form.save()
			return redirect("slot_list")
	else:
		form = AvailabilitySlotForm(instance=slot)

	return render(request, "services/slot_form.html", {"form": form, "title": "Editar horario"})


@user_passes_test(_is_staff)
def slot_delete(request, pk):
	slot = get_object_or_404(AvailabilitySlot, pk=pk)
	booking = getattr(slot, "booking", None)
	can_delete = booking is None or booking.status == "cancelled"
	if not can_delete:
		messages.error(request, "No puedes eliminar un horario con reserva asociada.")
		return redirect("slot_list")
	if request.method == "POST":
		if booking and booking.status == "cancelled":
			booking.delete()
		slot.delete()
		return redirect("slot_list")

	return render(
		request,
		"services/slot_confirm_delete.html",
		{"slot": slot, "can_delete": can_delete, "booking": booking},
	)


@user_passes_test(_is_staff)
def slot_delete_unreserved(request):
	if request.method == "POST":
		AvailabilitySlot.objects.filter(booking__isnull=True).delete()
		return redirect("slot_list")

	return render(request, "services/slot_confirm_delete_unreserved.html")


def _create_slots_from_form(data):
	start_date = data["start_date"]
	end_date = data["end_date"]
	start_time = data["start_time"]
	end_time = data["end_time"]
	slot_minutes = data["slot_minutes"]
	weekdays = data["weekdays"]

	current_date = start_date
	created_count = 0

	# Create slots day by day within the selected date range.
	while current_date <= end_date:
		if current_date.weekday() in weekdays:
			current_dt = datetime.combine(current_date, start_time)
			end_dt = datetime.combine(current_date, end_time)
			while current_dt < end_dt:
				next_dt = current_dt + timedelta(minutes=slot_minutes)
				if next_dt > end_dt:
					break

				_, created = AvailabilitySlot.objects.get_or_create(
					date=current_date,
					start_time=current_dt.time(),
					end_time=next_dt.time(),
					defaults={"is_active": True},
				)
				if created:
					created_count += 1

				current_dt = next_dt

		current_date += timedelta(days=1)

	return created_count
