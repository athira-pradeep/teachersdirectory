from django.forms import ModelForm
from .models import TeachersTable

class TeachersForm(ModelForm):
    class Meta:
        model = TeachersTable
        fields = '__all__'