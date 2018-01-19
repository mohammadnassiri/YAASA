from django.forms import ModelForm, TextInput
from analyze.models import Project


class CreateProject(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'file']
        labels = {
            'name': "Scan Name",
            'file': "Scan File"
        }
        error_messages = {
            'name': {
                'required': "This field is required.",
            },
            'file': {
                'required': "This field is required.",
            },
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Please enter an english name.', 'class': 'form-control'}),
        }


