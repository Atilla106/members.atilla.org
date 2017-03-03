from django.shortcuts import render

def legal_view(request):
	return render(request, 'legal.html')
