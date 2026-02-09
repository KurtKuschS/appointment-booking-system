from django.shortcuts import render

from .models import Service


def service_list(request):
	services = Service.objects.filter(is_active=True).order_by("name")
	context = {"services": services}
	return render(request, "services/service_list.html", context)
