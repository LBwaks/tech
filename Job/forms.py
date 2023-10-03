from django.utils import timezone
from typing import Any

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

# from taggit.forms import *
from taggit.models import Tag

from Account.models import Rating

from .models import Complaints, Job, JobImage


class JobForm(forms.ModelForm):
    """Form definition for Job."""

    required_css_class = "required"
    images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"required": False, "class": "form-control images", "multiple": True}
        ),
    )
    tags = forms.ModelMultipleChoiceField(
        label="Tags",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select form-control",
                "id": "job_tags",
                "required": True,
            }
        ),
        queryset=Tag.objects.all(),
    )

    content = forms.CharField(
        label="Descripion For The Job",
        widget=CKEditorWidget(attrs={"class": "form-control", "required": True}),
    )
    responsibility = forms.CharField(
        label="Responsibility For This Job",
        widget=CKEditorWidget(attrs={"class": "form-control", "required": True}),
    )
    qualification = forms.CharField(
        label="Qualification Needed For This Job",
        widget=CKEditorWidget(attrs={"class": "form-control", "required": True}),
    )

    skills = forms.CharField(
        label="Skills Needed For This Job",
        widget=CKEditorWidget(attrs={"class": "form-control", "required": True}),
    )

    class Meta:
        """Meta definition for Jobform."""

        model = Job
        fields = (
            "title",
            "category",
            "tags",
            "content",
            "responsibility",
            "qualification",
            "deadline",
            "job_end_time",
            "skills",
            "industry",
            "job_type",
            "seeker_type",
            "county",
            "location",
            "address",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "control-form title", "required": True}
            ),
            "category": forms.Select(
                attrs={"class": "control-select category", "required": True}
            ),
            "deadline": forms.DateTimeInput(
                attrs={
                    "class": "control-select deadline",
                    "required": True,
                    "type": "datetime-local",
                }
            ),
            "job_end_time": forms.DateTimeInput(
                attrs={
                    "class": "control-select job_end_time",
                    "required": True,
                    "type": "datetime-local",
                }
            ),
            "job_type": forms.Select(
                attrs={"class": "control-select job_type", "required": True}
            ),
            "seeker_type": forms.Select(
                attrs={"class": "control-select seeker_type", "required": True}
            ),
            "industry": forms.Select(
                attrs={"class": "control-select industry", "required": True}
            ),
            # "positions": forms.NumberInput(attrs={'min': '1', 'class': 'control-select positions', 'required': True}),
            "county": forms.Select(
                attrs={"class": "control-select county", "required": True}
            ),
            "location": forms.TextInput(
                attrs={"class": "control-form location", "required": True}
            ),
            "address": forms.TextInput(
                attrs={"class": "control-form address", "required": True}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        location = cleaned_data.get("location")
        address = cleaned_data.get("address")
        deadline = cleaned_data.get("deadline")
        job_end_time = cleaned_data.get("job_end_time")
        content = cleaned_data.get("content")
        responsibility = cleaned_data.get("responsibility")
        qualification = cleaned_data.get("qualification")
        skills = cleaned_data.get("skills")

        if title is not None and isinstance(title, str) and len(title) < 10:
            raise ValidationError(_("Title requires a minimum 10 characters required"), code="title")
        if location is not None and isinstance(location, str) and len(location) < 3:
            raise ValidationError(_("Location requires a minimum 3 characters required"), code="location")
        if address is not None and isinstance(address, str) and len(address) < 3:
            raise ValidationError(_("Address requires a minimum 3 characters required"), code="address")
        if content is not None and isinstance(content, str) and len(content) < 10:
            raise ValidationError(_("Description requires a minimum 10 characters required"), code="content")
        if (
            responsibility is not None
            and isinstance(responsibility, str)
            and len(responsibility) < 10
        ):
            raise ValidationError(
                _("Responsibility requires a minimum 10 characters required"), code="responsibility"
            )
        if (
            qualification is not None
            and isinstance(qualification, str)
            and len(qualification) < 10
        ):
            raise ValidationError(
                _("Minimum 10 characters required"), code="qualification"
            )
        if skills is not None and isinstance(skills, str) and len(skills) < 10:
            raise ValidationError(_("Skills requires a minimum 10 characters required"), code="skills")
        if deadline is not None and deadline < timezone.now():
            raise ValidationError(_("Deadline should be greater than now"))
        if job_end_time is not None and job_end_time <= timezone.now():
            raise ValidationError(_("Job Done date  should be greater than now"))
        if job_end_time and deadline is not None and job_end_time <deadline :
            raise ValidationError(_("Job Done time should be greater than deadline."))
            
    def clean_image(self):
        images = self.cleaned_data.get("images", False)
        if images:
            if images.size > 1*1024*1024:
                raise ValidationError(
                    _("Photo should be less than 5mbs"), code="invalid"
                )

        return images


class JobEditForm(forms.ModelForm):
    """Form definition for Job."""

    required_css_class = "required"
    images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"required": False, "class": "form-control images", "multiple": True}
        ),
    )
    tags = forms.ModelMultipleChoiceField(
        label="Tags",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select form-control ",
                "id": "job_tags",
                "multiple": "multiple",
                "required": True,
            }
        ),
        queryset=Tag.objects.all(),
    )

    content = forms.CharField(
        label="Descripion For The Job",
        widget=CKEditorWidget(attrs={"class": "form-control", "required": True}),
    )
    responsibility = forms.CharField(
        label="Responsibility For This Job",
        widget=CKEditorWidget(attrs={"class": "form-control", "required": True}),
    )
    qualification = forms.CharField(
        label="Qualification Needed For This Job",
        widget=CKEditorWidget(attrs={"class": "form-control", "required": True}),
    )
    skills = forms.CharField(
        label="Skills Needed For This Job",
        widget=CKEditorWidget(attrs={"class": "form-control", "required": True}),
    )

    class Meta:
        """Meta definition for Jobform."""

        model = Job
        fields = (
            "title",
            "category",
            "tags",
            "content",
            "responsibility",
            "qualification",
            "deadline",
            "job_end_time",
            "skills",
            "industry",
            "job_type",
            "seeker_type",
            # "positions",
            "county",
            "location",
            "address",
        )
        label = {
            # "positions":"Available slots",
        }
        # def __init__(self,*args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['title',].widget.attrs.update({'class':'form-label'})
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "control-form title", "required": True}
            ),
            "category": forms.Select(
                attrs={"class": "control-select category", "required": True}
            ),
            "deadline": forms.DateTimeInput(
                attrs={
                    "class": "control-select deadline",
                    "required": True,
                    "type": "datetime-local",
                }
            ),
            "job_end_time": forms.DateTimeInput(
                attrs={
                    "class": "control-select job_end_time",
                    "required": True,
                    "type": "datetime-local",
                }
            ),
            "job_type": forms.Select(
                attrs={"class": "control-select job_type", "required": True}
            ),
            "seeker_type": forms.Select(
                attrs={"class": "control-select seeker_type", "required": True}
            ),
            "industry": forms.Select(
                attrs={"class": "control-select industry", "required": True}
            ),
            # "positions": forms.NumberInput(attrs={'min': '1', 'class': 'control-select positions', 'required': True}),
            "county": forms.Select(
                attrs={"class": "control-select county", "required": True}
            ),
            "location": forms.TextInput(
                attrs={"class": "control-form location", "required": True}
            ),
            "address": forms.TextInput(
                attrs={"class": "control-form address", "required": True}
            ),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ("ratings", "reviews")
        labels = {"ratings": "Rate Applicant", "reviews": "Review Applicant"}
        widget = {
            "ratings": forms.Select(
                attrs={"class": "form-select ratings", "required": True}
            ),
            "reviews": forms.Textarea(
                attrs={"class": "form-control reviews", "required": True}
            ),
        }


class ComplaintsForm(forms.ModelForm):
    """ComplaintsForm definition."""

    # description=forms.CharField(label="Description ",widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    class Meta:
        model = Complaints
        fields = ("title", "subject", "description")
        labels = {"description": "Please describe you complaint or suggestion"}

        # TODO: Define form fields here
        widget = {
            "title": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "subjects": forms.Select(attrs={"class": "form-select", "required": True}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "required": True}
            ),
        }
