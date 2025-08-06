from django.shortcuts import render
from datetime import datetime






def home(request):
# Get today's date
    today = datetime.today().date()

    # Define the target date (November 2 of the current year)
    target_date = datetime(today.year, 11, 2).date()

    # Calculate the difference in days
    delta = (target_date - today).days

    # If target date has already passed this year, calculate days until Nov 2 next year
    if delta < 0:
        delta = 0

    return render(request, 'runway.html',{
        "Days_left": delta
    })



# Create your views here.
