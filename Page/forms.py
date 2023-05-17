from django import forms
from Job.models import Job
from django.utils.translation import gettext_lazy as _
from taggit.models import Tag

class JobSearchForm(forms.Form):
    tag =forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        empty_label=_('All Tags'),
        required= False,
        widget = forms.Select(attrs={'class':'form-control'})
    )
    title = forms.CharField(
        label=_("Title"),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        label=_("Location"),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

