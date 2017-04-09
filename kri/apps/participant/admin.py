from django.contrib import admin
from django.contrib.auth.models import User
from .models import University, Manager, Team, Person

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
