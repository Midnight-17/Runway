from django.shortcuts import render


def home(request):
    return render(request, 'runway.html')



# Create your views here.
