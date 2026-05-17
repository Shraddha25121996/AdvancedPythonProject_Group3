from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404
from django.core.files.storage import FileSystemStorage
from .repository import update_applicant_resume

from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from resume_classifier.skill_explainer import explain_skills
import json
from resume_classifier.fit_engine import decide_fit

from resume_classifier.resume_parser import extract_resume_text
#from resume_classifier.predictor import predict_resume_fit
from resume_classifier.predictor import predict_resume_category

from .forms import ApplicantForm
from .repository import (
    get_all_applicants,
    create_applicant,
    get_applicant_by_id,
    update_applicant,
    update_applicant_resume,
    update_applicant_classification,
)


@login_required
def applicant_list(request):
    applicants = get_all_applicants()

    return render(request, "applicants/applicant_list.html", {
        "applicants": applicants,
    })


@login_required
def applicant_create(request):
    if request.method == "POST":
        form = ApplicantForm(request.POST)

        if form.is_valid():
            try:
                create_applicant(form.cleaned_data)
                return redirect("applicants:list")
            except IntegrityError:
                form.add_error("email", "An applicant with this email already exists.")
    else:
        form = ApplicantForm()

    return render(request, "applicants/applicant_create.html", {
        "form": form,
    })


@login_required
def applicant_edit(request, applicant_id):
    applicant = get_applicant_by_id(applicant_id)

    if applicant is None:
        raise Http404("Applicant not found.")

    if request.method == "POST":
        form = ApplicantForm(request.POST)

        if form.is_valid():
            try:
                update_applicant(applicant_id, form.cleaned_data)

                uploaded_resume = request.FILES.get("resume_file")

                if uploaded_resume:
                    fs = FileSystemStorage(location="media/resumes")
                    saved_filename = fs.save(uploaded_resume.name, uploaded_resume)
                    resume_path = f"resumes/{saved_filename}"

                    update_applicant_resume(applicant_id, resume_path)

                return redirect("applicants:edit", applicant_id=applicant_id)

            except IntegrityError:
                form.add_error("email", "An applicant with this email already exists.")

    else:
        form = ApplicantForm(initial={
            "first_name": applicant["first_name"],
            "last_name": applicant["last_name"],
            "email": applicant["email"],
            "phone": applicant["phone"],
            "position_applied": applicant["position_applied"],
            "status": applicant["status"],
            "notes": applicant["notes"],
        })

    top_categories = []
    matched_skills = []
    missing_skills = []

    if applicant.get("matched_skills_json"):
        matched_skills = json.loads(applicant["matched_skills_json"])

    if applicant.get("missing_skills_json"):
        missing_skills = json.loads(applicant["missing_skills_json"])

    if applicant.get("top_categories_json"):
        try:
            top_categories = json.loads(applicant["top_categories_json"])
        except json.JSONDecodeError:
            top_categories = []

    return render(request, "applicants/applicant_edit.html", {
        "form": form,
        "applicant": applicant,
        "top_categories": top_categories,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    })

@login_required
def classify_resume(request, applicant_id):
    applicant = get_applicant_by_id(applicant_id)

    if applicant is None:
        raise Http404("Applicant not found.")

    if not applicant.get("resume_file"):
        messages.error(request, "Please upload a resume before running the classifier.")
        return redirect("applicants:edit", applicant_id=applicant_id)

    resume_path = settings.MEDIA_ROOT / applicant["resume_file"]

    extracted_text = extract_resume_text(str(resume_path))
    #result = predict_resume_fit(extracted_text)
    result = predict_resume_category(extracted_text)

    skill_result = explain_skills(
        resume_text=extracted_text,
        predicted_category=result["predicted_category"],
    )

    fit_result = decide_fit(
        predicted_category=result["predicted_category"],
        category_confidence=result["category_confidence"],
        position_applied=applicant["position_applied"],
    )

    fit_explanation = (
        f"{fit_result['fit_explanation']} "
        f"The resume matched {skill_result['matched_count']} out of "
        f"{skill_result['total_skills']} expected skills for this category."
    )

    top_categories_json = json.dumps(result["top_categories"])


    #update_applicant_classification(
    #    applicant_id=applicant_id,
    #    prediction=result["prediction"],
    ##    confidence=result["confidence"],
    #    classified_at=timezone.now(),
    #    explanation=result["explanation"],
    #)

    update_applicant_classification(
        applicant_id=applicant_id,
        prediction=result["predicted_category"],
        confidence=result["category_confidence"],
        classified_at=timezone.now(),
        explanation=None,
        top_categories_json=json.dumps(result["top_categories"]),
        fit_label=fit_result["fit_label"],
        fit_explanation=fit_explanation,
        matched_skills_json=json.dumps(skill_result["matched_skills"]),
        missing_skills_json=json.dumps(skill_result["missing_skills"]),
    )

    messages.success(request, "Resume classified successfully.")
    return redirect("applicants:edit", applicant_id=applicant_id)