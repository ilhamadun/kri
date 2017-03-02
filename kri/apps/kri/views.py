"""Views for kir app"""

from django.shortcuts import render


def index(request):
    """Render home page"""
    return render(request, 'kri/index.html')
