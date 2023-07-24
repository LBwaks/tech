from typing import Any, Dict
from django import forms

class EmailForm(forms.Form):
    """EmailForm definition."""

    # TODO: Define form fields here
    email = forms.EmailField(label="Email", required=True)
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email') 
        return super().clean()