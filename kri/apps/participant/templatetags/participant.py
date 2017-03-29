from django import template
from kri.apps.participant.forms import PersonForm
from kri.apps.participant.models import Person


register = template.Library()

@register.inclusion_tag('participant/person-form-panel.html', name='person_form_panel')
def person_form_panel(person, counter):
    """Render PersonForm in template with context"""
    return {
        'form': PersonForm(instance=person),
        'team_id': person.team.id,
        'person_id': person.id,
        'person_type': person.type,
        'person_type_display': Person.person_type_display(person.type),
        'person_type_count': counter,
        'collapsed': counter > 1
    }
