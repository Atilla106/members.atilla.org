from django.shortcuts import render

from .models import CleaningRoster


def portal_view(request):
    rosters = CleaningRoster.objects.all()
    print(list(rosters)[0].cleaners.all())
    return render(request, "cleaning/portal.html", {'rosters': rosters})
