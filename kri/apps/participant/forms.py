from django.forms import ModelForm, HiddenInput
from .models import Team, Person


class TeamForm(ModelForm):
    """Team model Form for registration"""
    class Meta:
        model = Team
        fields = ['name', 'arrival_time', 'transport', 'photo']

class PersonForm(ModelForm):
    """Person model Form for registration"""
    class Meta:
        model = Person
        fields = ['name', 'type', 'instance_id', 'birthday', 'gender', 'phone',
                  'email', 'shirt_size']
        widgets = {
            'type': HiddenInput()
        }
