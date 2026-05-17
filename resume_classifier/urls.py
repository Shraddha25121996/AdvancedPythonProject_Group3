from django.urls import path
from .views import upload_resume

app_name = "resume_classifier"

urlpatterns = [
    path("upload/", upload_resume, name="upload"),
]