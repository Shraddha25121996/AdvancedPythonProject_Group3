from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .forms import ResumeUploadForm
#from .predictor import predict_resume_fit
from .resume_parser import extract_resume_text


def upload_resume(request):
    form = ResumeUploadForm()
    result = None
    extracted_text_preview = None

    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data["resume_file"]

            fs = FileSystemStorage()
            saved_filename = fs.save(uploaded_file.name, uploaded_file)
            saved_file_path = fs.path(saved_filename)

            extracted_text = extract_resume_text(saved_file_path)
            extracted_text_preview = extracted_text[:1000]

            result = None#predict_resume_fit(extracted_text)

            return render(request, "resume_classifier/upload.html", {
                "form": form,
                "result": result,
                "uploaded_file_name": uploaded_file.name,
                "extracted_text_preview": extracted_text_preview,
            })

    return render(request, "resume_classifier/upload.html", {
        "form": form,
        "result": result,
        "extracted_text_preview": extracted_text_preview,
    })