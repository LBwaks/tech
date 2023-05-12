from ckeditor.widgets import CKEditorWidget
from django import forms

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Profile, ProfileCV


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


# class PhoneForm(forms.Form):
#     number = PhoneNumberField(region="CA")


# class CanadianPhoneForm(forms.Form):
#     # RegionalPhoneNumberWidget is the default widget.

#     number = PhoneNumberField(region="CA")


# from django import forms
# from phonenumber_field.formfields import PhoneNumberField
# from phonenumber_field.widgets import PhoneNumberPrefixWidget

# # Limiting country choices.


# class CanadianPhoneForm(forms.Form):
#     # RegionalPhoneNumberWidget is the default widget.

#     number = PhoneNumberField(
#         region="CA",
#         widget=PhoneNumberPrefixWidget(
#             country_choices=[
#                 ("CA", "Canada"),
#                 ("FR", "France"),
#             ],
#         ),
#     )
