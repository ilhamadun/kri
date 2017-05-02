from django.forms import ModelForm, HiddenInput, DateInput, DateTimeField, FileInput
from django.contrib.auth.models import User
from .models import Team, Person, Manager, Supporter


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = ['name', 'phone', 'requested_university', 'student_card']

class TeamForm(ModelForm):
    """Team model Form for registration"""
    arrival_time = DateTimeField(widget=DateInput(format='%d/%m/%Y %H:%M',
                                                  attrs={'class': 'form-control arrival-time'}),
                                 input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Team
        fields = ['name', 'arrival_time', 'transport']


class PersonForm(ModelForm):
    """Person model Form for registration"""
    birthday = DateTimeField(
        widget=DateInput(format='%d/%m/%Y', attrs={'class': 'form-control birthday'}),
        input_formats=['%d/%m/%Y'])

    class Meta:
        model = Person
        fields = ['name', 'type', 'instance_id', 'birthday', 'gender', 'phone',
                  'email', 'photo']
        widgets = {
            'type': HiddenInput(),
            'photo': FileInput()
        }

class SupporterForm(ModelForm):
    class Meta:
        model = Supporter
        fields = ['amount']
