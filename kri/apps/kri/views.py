"""Views for kir app"""

from django.shortcuts import render
from django.http import Http404


def index(request):
    """Render home page"""
    return render(request, 'kri/index.html')


def informasi(request, page=None):
    pages = (
        'buku-panduan',
        'peraturan-peserta',
        'tata-tertib-penonton',
        'tata-tertib-pers')

    if page in pages:
        return render(request, 'kri/' + page + '.html')
    else:
        raise Http404
