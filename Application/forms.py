from django import forms 
from .models import Application
from Job.models import Job
from ckeditor.widgets import CKEditorWidget
class ApplicationForm(forms.ModelForm):
    """Form definition for Application."""
    description = (forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control''required'}),))
    class Meta:
        """Meta definition for Applicationform."""

        model = Application
        fields = ('charge','description')
        widget ={
            'charge':forms.NumberInput(attrs={'class':'form-select charge''required'}),
            # 'job': forms.HiddenInput(), 
            
        }
    # def __init__(self, *args, **kwargs):
    #     slug = kwargs.pop('slug')
    #     super().__init__(*args, **kwargs)
    #     self.fields['job'].queryset = Job.objects.filter(slug=slug)

class ApplicationEditForm(forms.ModelForm):
    """Form definition for Application."""
    description = (forms.CharField(widget=CKEditorWidget(attrs={'class':'form-control''required'}),))
    class Meta:
        """Meta definition for Applicationform."""

        model = Application
        fields = ('charge','description')
        widget ={
            'charge':forms.NumberInput(attrs={'class':'form-select charge''required'}),
            # 'job': forms.HiddenInput(), 
            
        }