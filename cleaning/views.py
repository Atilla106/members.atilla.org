from django.shortcuts import render

from .models import CleaningRoster


def portal_view(request):
    rosters = CleaningRoster.objects.all()
    return render(request, "cleaning/portal.html", {'rosters': rosters})
