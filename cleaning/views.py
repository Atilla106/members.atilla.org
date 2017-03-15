from accounts.models import Account
from django.shortcuts import render
from random import sample


def portalView(request):
    volunteers = list(Account.objects.filter(cleaning=True))
    cleaners = sample(volunteers, 3)
    return render(request, "cleaning/portal.html", {'cleaners': cleaners})
