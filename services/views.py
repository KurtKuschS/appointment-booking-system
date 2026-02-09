from datetime import datetime, timedelta

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from .forms import BulkSlotForm
from .models import AvailabilitySlot, Service


def service_list(request):
	services = Service.objects.filter(is_active=True).order_by("name")
	context = {"services": services}
	return render(request, "services/service_list.html", context)


def _is_staff(user):
	return user.is_staff


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
