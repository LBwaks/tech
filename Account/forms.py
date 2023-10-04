from typing import Any
from ckeditor.widgets import CKEditorWidget
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Education, Profile, ProfileCV,Experience
from django.utils.translation import gettext as _


class  ProfileForm(forms.ModelForm):
   
    documents = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'required': False,
        'class': 'form-control cv',
        'multiple': True,
    }), label='Upload documents', help_text='Select one or more documents to upload.')

    bio = (forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control''required'}),)),    
    
    tell = PhoneNumberField(
        region="KE",
        
    )
    class Meta:
        model = Profile
        fields = (
            "firstname",
            "lastname",
            "title",
            "user_type",
            "id_passport",
            "tell",
            "gender",
            "dob",
            "county",
            "location",
            "address",
            "skills",
            "bio",
            "profile",
            "twitter",
            "facebook",
            "facebook",
            "website",
        )
        widgets ={
            "firstname":forms.TextInput(attrs={'class':'form-class firstname','required':True}),
            "lastname":forms.TextInput(attrs={'class':'form-class lastname','required':True}),
            "title":forms.TextInput(attrs={'class':'form-class lastname','required':True,'placeholder':'eg, Carpenter Plumber'}),
            "user_type":forms.Select(attrs={'class':'form-class user_type','required':True}),
            "id_passport":forms.NumberInput(attrs={'class':'form-class id_passport','required':True}),
           
            "gender":forms.Select(attrs={'class':'form-class firstname','required':True}),
            "dob":forms.DateInput(attrs={'class': 'control-select deadline', 'required': True, 'type': 'date'}),
            "county":forms.Select(attrs={'class':'form-class firstname','required':True}),
            "location":forms.TextInput(attrs={'class':'form-class location','required':True}),
            "address":forms.TextInput(attrs={'class':'form-class address','required':True}),
            "skills":forms.TextInput(attrs={'class':'form-class skills','required':True}),
            "profile": forms.ClearableFileInput(attrs={"class": "form-control","accept":".png,.jpg,.jpeg"}),
            "twitter": forms.URLInput(attrs={"class": "form-control twitter"}),
            "facebook": forms.URLInput(attrs={"class": "form-control facebook"}),
            "instagram": forms.URLInput(attrs={"class": "form-control instagram"}),
            "website": forms.URLInput(attrs={"class": "form-control website"}),
            
        }

class EducationForm(forms.ModelForm):
    
    class Meta:
        model = Education
        fields = ("course","institution","description","start_date","end_date")
        widgets ={
            "course":forms.TextInput(attrs={'class':'form-class course','required':True}),
            "institution":forms.TextInput(attrs={'class':'form-class institution','required':True}),
            "description":forms.Textarea(attrs={'class':'form-class description',}),
            "start_date":forms.DateInput(attrs={'class': 'control-select start_date', 'required': True, 'type': 'date'}),
            "end_date":forms.DateInput(attrs={'class': 'control-select end_date', 'type':"date"}),
        }
    def clean(self):
        cleaned_data= super().clean()
        start_date= cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if (start_date is not None and end_date is not None) and start_date  >= end_date:
            raise ValidationError(_('Start Date shuold should not be greater than end date '))
        
class ExperienceForm(forms.ModelForm):
    
    class Meta:
        model = Experience
        fields = ("title","employer","description","start_date","end_date")
        widgets ={
            "title":forms.TextInput(attrs={'class':'form-class title','required':True}),
            "employer":forms.TextInput(attrs={'class':'form-class employer','required':True}),
            "description":forms.Textarea(attrs={'class':'form-class description',}),
            "start_date":forms.DateInput(attrs={'class': 'control-select start_date', 'required': True, 'type': 'date'}),
            "end_date":forms.DateInput(attrs={'class': 'control-select end_date', 'type':"date"}),
        }
    def clean(self):
        cleaned_data= super().clean()
        start_date= cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if (start_date is not None and end_date is not None) and start_date  >= end_date:
            raise ValidationError(_('Start Date should should not be greater than end date '))
