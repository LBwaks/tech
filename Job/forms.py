from django import forms
from .models import Job,JobImage
from taggit.forms import *
from taggit.models import Tag
from ckeditor.widgets import CKEditorWidget


class JobForm(forms.ModelForm):
    """Form definition for Job."""
    images= forms.FileField(required=False, widget=forms.FileInput(attrs={
        'required': False,
        'class': 'form-control images',
        'multiple': True
    }))
    tags = forms.ModelMultipleChoiceField(label="Tags", widget=forms.SelectMultiple(attrs={"class":"form-select  form-control tag-multiple" ,"style":"width:100%" ,"multiple":'multiple' "required"}),queryset=Tag.objects.all())
   
    content = (forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control''required'}),))
    skills = (forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control''required'}),))

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
           
            "job_type",
            "seeker_type",
            "positions",
            "county",
            "location",
            "address",
        )
        widgets ={
             "title":forms.TextInput(attrs={'class':'control-form title' 'required'}),
            "category":forms.Select(attrs={'class':'control-select category' 'required'}),
            
            "deadline":forms.DateTimeInput(attrs={'class':'control-select deadline' 'required','type': 'datetime-local'}),
            "job_end_time":forms.DateTimeInput(attrs={'class':'control-select job_end_time' 'required','type': 'datetime-local'}),
           
           
            "job_type":forms.Select(attrs={'class':'control-select job_type' 'required'}),
            "seeker_type":forms.Select(attrs={'class':'control-select seeker_type' 'required'}),
            "positions":forms.NumberInput(attrs={'min':'1','class':'control-select positions' 'required'}),
            "county":forms.Select(attrs={'class':'control-select county' 'required'}),
            "location":forms.TextInput(attrs={'class':'control-form location' 'required'}),
            "address":forms.TextInput(attrs={'class':'control-form address' 'required'}),
        }