from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from applicants.repository import count_applicants

@login_required
def index(request):
    total_applicants = count_applicants()

    return render(request, "dashboard/index.html", {
          "total_applicants": total_applicants,
    })