from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import has_access
from .forms import TeamForm, PersonForm
from .models import Team


@login_required
def index(request):
    return render(request, 'participant/index.html', {
        'has_access': request.user.university.all_access()
    })


def division(request, *args, **kwargs):
    try:
        instance = request.user.university.team(kwargs['division'])
    except Team.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form_team = TeamForm(request.POST, request.FILES, instance=instance)

        if form_team.is_valid():
            team = form_team.save(commit=False)
            team.university = request.user.university
            team.division = kwargs['division']
            team.save()
            messages.success(request, 'Informasi tim telah disimpan.')

        else:
            messages.error(request, 'Ada kesalahan dalam formulir Anda.')

    else:
        form_team = TeamForm(instance=instance)

    return render(request, 'participant/division.html', {
        'active': kwargs['division'],
        'title': kwargs['title'],
        'has_access': request.user.university.all_access(),
        'form_team': form_team
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
