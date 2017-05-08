from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Card, CardLog


def logger(request, activity):
    username = request.POST['username']
    password = request.POST['password']
    card_key = request.POST['card_key']
    user = authenticate(username=username, password=password)

    if user is not None:
        try:
            cardlog = CardLog.create_log(card_key, activity, user)

            if cardlog.activity == (activity + '_granted'):
                return JsonResponse({
                    'activity': activity,
                    'status': 'success',
                    'message': activity.capitalize() + ' granted.',
                    'person': {
                        'name': cardlog.card.person.name,
                        'gender': cardlog.card.person.gender,
                        'team': cardlog.card.person.team.name,
                        'division': cardlog.card.person.get_type_display(),
                        'role': cardlog.card.person.type,
                        'university': cardlog.card.person.team.university.name
                    }
                })
            elif cardlog.activity == (activity + '_denied'):
                return JsonResponse({
                    'activity': activity,
                    'status': 'denied',
                    'message': activity.capitalize() + ' denied.'
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


@login_required
def fetch_log(request):
    log = CardLog.last_by_admin(request.user)

    if log is not None:
        try:
            photo = log.card.person.photo.url
        except ValueError:
            photo = None

        return JsonResponse({
            'status': log.activity,
            'time': log.time,
            'person': {
                'name': log.card.person.name,
                'team': log.card.person.team.name,
                'division': log.card.person.team.get_division_display(),
                'university': log.card.person.team.university.name,
                'photo': photo,
            }
        })

    return HttpResponse(status=204)
