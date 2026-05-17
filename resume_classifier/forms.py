from django import forms


class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        label="Upload Resume",
        help_text="Only PDF and DOCX files are allowed."
    )

    def clean_resume_file(self):
        file = self.cleaned_data["resume_file"]

        allowed_extensions = [".pdf", ".docx"]

        if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError("Only PDF and DOCX files are allowed.")

        return file