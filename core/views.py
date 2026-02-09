from django.shortcuts import render

from pages.models import AboutPage
from services.models import Service


def home(request):
    services = Service.objects.filter(is_active=True).order_by("name")[:3]
    return render(request, "home.html", {"services": services})


def about(request):
    about_page = AboutPage.objects.prefetch_related("photos").first()
    return render(request, "about.html", {"about": about_page})
