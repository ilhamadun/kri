from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.models import User
from .decorators import has_access
from .forms import RegistrationForm, ManagerForm, TeamForm, PersonForm
from .models import Team, Person, University, Manager


def login(request):
    context = {
        'university': University.objects.filter(user=None)
    }

    if request.method == 'POST':
        if request.POST['action'] == 'register':
            form_registration = RegistrationForm(request.POST)
            form_manager = ManagerForm(request.POST)
            if form_registration.is_valid() and form_manager.is_valid():
                user = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                request.POST['password'])
                user.is_active = False
                user.save()

                Manager.objects.create(
                    user=user,
                    phone=request.POST['phone'],
                    requested_university=University.objects.get(pk=request.POST['requested_university']))

                messages.success(request, "Pendaftaran Anda sedang diverifikasi oleh panitia. Selanjutnya Anda akan dihubungi oleh LO.")

            else:
                context['register_error'] = True

        elif request.POST['action'] == 'login':
            return auth_login(request, template_name='participant/login.html')


    if request.GET.get('next', False):
        context['next'] = request.GET['next']

    return render(request, 'participant/login.html', context)


@login_required
def index(request):
    teams = {}
    for t in Team.TEAM_DIVISION:
        try:
            teams[t[0]] = request.user.university.team(t[0])
        except Team.DoesNotExist:
            teams[t[0]] = None

    return render(request, 'participant/index.html', {
        'has_access': request.user.university.all_access(),
        'teams': teams,
    })


@login_required
@has_access('krai')
def krai(request):
    return division(request, division='krai', title='Kontes Robot ABU Indonesia')


@login_required
@has_access('krsbi_beroda')
def krsbi_beroda(request):
    return division(request, division='krsbi_beroda',
                    title='Kontes Robot Sepak Bola Beroda Indonesia')


@login_required
@has_access('krsti')
def krsti(request):
    return division(request, division='krsti', title='Kontes Robot Seni Tari Indonesia')


@login_required
@has_access('krpai')
def krpai(request):
    return division(request, division='krpai', title='Kontes Robot Pemadam Api Indonesia')


def division(request, **kwargs):
    """Handle request for Team creation"""
    try:
        instance = request.user.university.team(kwargs['division'])
    except Team.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form_team = TeamForm(request.POST, request.FILES, instance=instance)

        response_data = {'photo': None}
        if form_team.is_valid():
            team = form_team.save(commit=False)
            team.university = request.user.university
            team.division = kwargs['division']
            team.save()
            response_data['status'] = 'success'
            response_data['message'] = 'Informasi tim telah disimpan.'
            response_data['team_id'] = team.id

            if team.photo:
                response_data['photo'] = team.photo.url

        else:
            response_data['status'] = 'error'
            response_data['message'] = 'Ada kesalahan dalam formulir Anda.'

        if request.is_ajax():
            return JsonResponse(response_data)
        else:
            getattr(messages, response_data['status'])(request, response_data['message'])

    else:
        form_team = TeamForm(instance=instance)

        members = {
            'core_member': [],
            'mechanics': [],
            'adviser': [],
        }
        if instance:
            for m in instance.persons.all():
                members[m.type].append(m)

    return render(request, 'participant/division.html', {
        'active': kwargs['division'],
        'title': kwargs['title'],
        'has_access': request.user.university.all_access(),
        'team': instance,
        'form_team': form_team,
        'members': members
    })


@login_required
def person(request, person_type):
    """Handle request on person creation

    The action will depend on the HTTP method:
        - POST: try to save the form to a Person
        - Get: render PersonForm

    Raises:
        - Http404: person_type is not in Person.PERSON_TYPE or request is not ajax

    """
    if not person_type in ('core_member', 'mechanics', 'adviser') or not request.is_ajax():
        raise Http404

    if request.method == 'POST':
        return person_form_submission(request, person_type)
    else:
        return render_person_form(request, person_type)


def person_form_submission(request, person_type):
    """Handle PersonForm submission from request"""
    instance = get_person(request.POST['person_id'])
    member = save_person(request, person_type, instance)

    response_data = {}
    if member:
        response_data['person_id'] = member.id
        response_data['status'] = 'success'

        if member.photo:
            response_data['photo'] = member.photo.url

        if instance:
            response_data['message'] = Person.person_type_display(person_type) + ' berhasil diubah.'
        else:
            response_data['message'] = Person.person_type_display(person_type) + ' berhasil ditambahkan.'

    else:
        response_data['status'] = 'error'
        response_data['message'] = 'Gagal menambahkan ' + Person.person_type_display(person_type)

    return JsonResponse(response_data)


def get_person(person_id):
    """Try to get a Person from given person id"""
    try:
        if person_id != '':
            instance = Person.objects.get(pk=person_id)
        else:
            instance = None
    except (Person.DoesNotExist, IndexError):
        instance = None

    return instance


def save_person(request, person_type, instance):
    """Submit PersonForm from request"""
    member = None
    form_person = PersonForm(request.POST, request.FILES, instance=instance)

    if form_person.is_valid():
        member = form_person.save(commit=False)
        member.team = Team.objects.get(pk=request.POST['team_id'])
        member.type = person_type
        member.save()
    else:
        print(form_person.errors)

    return member


def render_person_form(request, person_type):
    """Render PersonForm with detailed context"""
    team = Team.objects.get(pk=request.GET['team_id'])
    available_slot = team.available_slot(person_type)
    if available_slot:
        return render(request, 'participant/person-form-panel.html', {
            'form': PersonForm(),
            'team_id': team.id,
            'person_type': person_type,
            'person_type_display': Person.person_type_display(person_type),
            'person_type_count': getattr(team, person_type)().count() + 1,
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': Person.person_type_display(person_type) + ' sudah penuh.'
        })
