from django.urls import path
from . import views

app_name = "applicants"

urlpatterns = [
    path("", views.applicant_list, name="list"),
    path("create/", views.applicant_create, name="create"),
    path("<int:applicant_id>/edit/", views.applicant_edit, name="edit"),
    path("<int:applicant_id>/classify-resume/", views.classify_resume, name="classify_resume"),
]