
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators

# strip means to remove whitespace from the beginning and the end before storing the column
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

from .models import Project

from django import forms

class ProjectForm(forms.ModelForm):
    techs = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'e.g., C#, Python3, JavaScript'}),
        label="List of Technologies Used",
        help_text='Enter technologies separated by commas.'
    )
    repo = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'https://github.com/'}),
        label="Repository Address"
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe the project', 'rows': 3}),
        label="Project Description",
        help_text='Describe the project and the skills, development process or your feedback.'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write something...', 'rows': 3}),
        label="Project Notes", required=False,
        help_text='What you practiced in the project and what you would like to do more.'
    )

    class Meta:
        model = Project
        fields = ['title', 'text', 'tags', 'repo', 'category', 'techs', 'requirement', 'status', 'notes']  # Specify fields explicitly for clarity

    def clean_repo(self):
        repo = self.cleaned_data.get('repo')
        if not repo.startswith(('http://', 'https://')):
            raise forms.ValidationError("The repository URL must start with http:// or https://")
        return repo

    def clean_techs(self):
        techs = self.cleaned_data.get('techs')
        if not techs:
            raise forms.ValidationError("This field cannot be empty.")

        # Split the string by commas and validate
        words = techs.split(',')
        for word in words:
            word = word.strip()  # Remove any extra spaces
            if not word:
                raise forms.ValidationError(
                    "Technologies must be separated by commas without empty entries."
                )

        return techs
