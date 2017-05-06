from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import Card, CardLog


def logger(request, activity):
    username = request.POST['username']
    password = request.POST['password']
    card_key = request.POST['card_key']
    user = authenticate(username=username, password=password)

    if user is not None:
        try:
            cardlog = CardLog.create_log(card_key, activity, user)

            if cardlog:
                return JsonResponse({
                    'activity': activity,
                    'status': 'success',
                    'message': activity.capitalize() + ' success.',
                    'person': {
                        'name': cardlog.card.person.name,
                        'gender': cardlog.card.person.gender,
                        'team': cardlog.card.person.team.name,
                        'division': cardlog.card.person.get_type_display(),
                        'role': cardlog.card.person.type,
                        'university': cardlog.card.person.team.university.name
                    }
                })
            else:
                return JsonResponse({
                    'activity': activity,
                    'status': 'failed',
                    'message': activity.capitalize() + ' rejected.'
                })
        except Card.DoesNotExist:
            return JsonResponse({
                'activity': activity,
                'status': 'failed',
                'message': 'Card not recognized.'
            })

        return JsonResponse({
            'activity': activity,
            'status': 'failed',
            'message': activity.capitalize() + ' failed.'
        })
    else:
        return JsonResponse({
            'activity': activity,
            'status': 'failed',
            'message': 'Authentication failed.'
        })


def login(request):
    return logger(request, 'login')


def logout(request):
    return logger(request, 'logout')
