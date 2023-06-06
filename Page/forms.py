from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from taggit.models import Tag

from .models import Contact


class JobSearchForm(forms.Form):
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        empty_label=_("All Tags"),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    title = forms.CharField(
        label=_("Title"),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    location = forms.CharField(
        label=_("Location"),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class ContactForm(forms.ModelForm):
    """Form definition for Contact."""

    class Meta:
        """Meta definition for Contactform."""

        model = Contact
        fields = (
            "name",
            "email",
            "subject",
            "message",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control name" "required"}),
            "email": forms.EmailInput(attrs={"class": "form-control email" "required"}),
            "message": forms.Textarea(
                attrs={"class": "form-control message" "required"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control subject" "required"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 3:
            raise ValidationError(
                _("Name should be more than 3 characters"), code="invalid"
            )
        return name

    def clean_message(self):
        message = self.cleaned_data["message"]
        if len(message) < 10:
            raise ValidationError(
                _("Message should be more than 10 characters"), code="invalid"
            )
        return message

    def clean_content(self):
        content = self.cleaned_data["content"]
        if len(content) < 10:
            raise ValidationError(
                _("cDescription should be more than 10 characters"), code="invalid"
            )
        return content
