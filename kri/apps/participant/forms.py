from django.forms import ModelForm, HiddenInput, DateInput, DateTimeField
from .models import Team, Person


class TeamForm(ModelForm):
    """Team model Form for registration"""
    arrival_time = DateTimeField(widget=DateInput(format='%d/%m/%Y %H:%M',
                                                  attrs={'class': 'form-control arrival-time'}),
                                 input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Team
        fields = ['name', 'arrival_time', 'transport', 'photo']

class PersonForm(ModelForm):
    """Person model Form for registration"""
    birthday = DateTimeField(widget=DateInput(format='%d/%m/%Y', attrs={'class': 'form-control birthday'}),
                             input_formats=['%d/%m/%Y'])

    class Meta:
        model = Person
        fields = ['name', 'type', 'instance_id', 'birthday', 'gender', 'phone',
                  'email', 'shirt_size']
        widgets = {
            'type': HiddenInput()
        }
