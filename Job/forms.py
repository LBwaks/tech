from django import forms
from .models import Job,JobImage
from taggit.forms import *
from taggit.models import Tag
from ckeditor.widgets import CKEditorWidget
from Application.models import Rating

class JobForm(forms.ModelForm):
    """Form definition for Job."""
    required_css_class = 'required'
    images= forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'required': False,
        'class': 'form-control images',
        'multiple': True
    }))
    tags = forms.ModelMultipleChoiceField(label="Tags", widget=forms.SelectMultiple(attrs={"class": "form-select form-control tag-multiple", "style": "width:100%", "multiple": "multiple", "required": True}), queryset=Tag.objects.all())
   
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    responsibility = forms.CharField(widget=CKEditorWidget( config_name='non_main', attrs={'class': 'form-control', 'required': True}))
    qualification = forms.CharField(widget=CKEditorWidget(config_name='non_main',attrs={'class': 'form-control', 'required': True}))
    
    skills = forms.CharField(widget=CKEditorWidget(config_name='non_main',attrs={'class': 'form-control', 'required': True}))

    class Meta:
        """Meta definition for Jobform."""

        model = Job
        fields = (
            "title",
            "category",
            "tags",
            "content",
            "responsibility",
            'qualification',
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
    required_css_class = 'required'
    images= forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'required': False,
        'class': 'form-control images',
        'multiple': True
    }))
    tags = forms.ModelMultipleChoiceField(label="Tags", widget=forms.SelectMultiple(attrs={"class": "form-select form-control tag-multiple", "style": "width:100%", "multiple": "multiple", "required": True}), queryset=Tag.objects.all())
   
    content = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    responsibility = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    qualification = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))
    skills = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'required': True}))

    class Meta:
        """Meta definition for Jobform."""

        model = Job
        fields = (
            "title",
            "category",
            "tags",
            "content",
            "responsibility",
            'qualification',
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
        # def __init__(self,*args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['title',].widget.attrs.update({'class':'form-label'})
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
        
class RatingForm(forms.ModelForm):
    
    class Meta:
        model = Rating
        fields = ("ratings","reviews")
        labels ={
            'ratings':'Rate Applicant',
            'reviews':'Review Applicant'
        }
        widget={
            'ratings': forms.Select(attrs={'class': 'form-control ratings', 'required': True}),
            'reviews': forms.Textarea(attrs={'class': 'form-control reviews', 'required': True})
        }
