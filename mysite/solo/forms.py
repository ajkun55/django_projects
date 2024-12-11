from django.forms import ModelForm
from solo.models import Fields


# Create the form class.
class FieldForm(ModelForm):
    class Meta:
        model = Fields
        fields = '__all__'
