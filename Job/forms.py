from django import forms
from .models import Job,JobImage
from taggit.forms import *
from taggit.models import Tag
from ckeditor.widgets import CKEditorWidget


class JobForm(forms.ModelForm):
    """Form definition for Job."""
    images= forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'required': False,
        'class': 'form-control images',
        'multiple': True
    }))
    tags = forms.ModelMultipleChoiceField(label="Tags", widget=forms.SelectMultiple(attrs={"class": "form-select form-control tag-multiple", "style": "width:100%", "multiple": "multiple", "required": True}), queryset=Tag.objects.all())
   
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    skills = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        """Meta definition for Jobform."""

        model = Job
        fields = (
            "title",
            "category",
            "tags",
            "content",
            "deadline",
            "job_end_time",
            "skills",
            'industry',
            "job_type",
            "seeker_type",
            "positions",
            "county",
            "location",
            "address",
        )
        widgets ={
            "title": forms.TextInput(attrs={'class': 'control-form title', 'required': True}),
            "category": forms.Select(attrs={'class': 'control-select category', 'required': True}),
            "deadline": forms.DateTimeInput(attrs={'class': 'control-select deadline', 'required': True, 'type': 'datetime-local'}),
            "job_end_time": forms.DateTimeInput(attrs={'class': 'control-select job_end_time', 'required': True, 'type': 'datetime-local'}),
            "job_type": forms.Select(attrs={'class': 'control-select job_type', 'required': True}),
            "seeker_type": forms.Select(attrs={'class': 'control-select seeker_type', 'required': True}),
            "industry": forms.Select(attrs={'class': 'control-select industry', 'required': True}),
            "positions": forms.NumberInput(attrs={'min': '1', 'class': 'control-select positions', 'required': True}),
            "county": forms.Select(attrs={'class': 'control-select county', 'required': True}),
            "location": forms.TextInput(attrs={'class': 'control-form location', 'required': True}),
            "address": forms.TextInput(attrs={'class': 'control-form address', 'required': True}),
        }
class JobEditForm(forms.ModelForm):
    """Form definition for Job."""
    images= forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'required': False,
        'class': 'form-control images',
        'multiple': True
    }))
    tags = forms.ModelMultipleChoiceField(label="Tags", widget=forms.SelectMultiple(attrs={"class": "form-select form-control tag-multiple", "style": "width:100%", "multiple": "multiple", "required": True}), queryset=Tag.objects.all())
   
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    skills = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        """Meta definition for Jobform."""

        model = Job
        fields = (
            "title",
            "category",
            "tags",
            "content",
            "deadline",
            "job_end_time",
            "skills",  
            'industry',         
            "job_type",
            "seeker_type",
            "positions",
            "county",
            "location",
            "address",
        )
        widgets ={
            "title": forms.TextInput(attrs={'class': 'control-form title', 'required': True}),
            "category": forms.Select(attrs={'class': 'control-select category', 'required': True}),
            "deadline": forms.DateTimeInput(attrs={'class': 'control-select deadline', 'required': True, 'type': 'datetime-local'}),
            "job_end_time": forms.DateTimeInput(attrs={'class': 'control-select job_end_time', 'required': True, 'type': 'datetime-local'}),
            "job_type": forms.Select(attrs={'class': 'control-select job_type', 'required': True}),
            "seeker_type": forms.Select(attrs={'class': 'control-select seeker_type', 'required': True}),
            "industry": forms.Select(attrs={'class': 'control-select industry', 'required': True}),
            "positions": forms.NumberInput(attrs={'min': '1', 'class': 'control-select positions', 'required': True}),
            "county": forms.Select(attrs={'class': 'control-select county', 'required': True}),
            "location": forms.TextInput(attrs={'class': 'control-form location', 'required': True}),
            "address": forms.TextInput(attrs={'class': 'control-form address', 'required': True}),
        }        