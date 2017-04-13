from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
from .models import University, Manager, Team, Person

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_to_manager', 'krai', 'krsbi_beroda', 'krsti', 'krpai',
                    'is_complete')

    def link_to_manager(self, obj):
        """Returns a link to university's manager"""
        if obj.user:
            link = urlresolvers.reverse('admin:participant_manager_change',
                                        args=[obj.user.manager.id])
            return format_html('<a href="{}">{}</a>', link, obj.user)
        else:
            return None

    link_to_manager.short_description = 'Manager'


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'email', 'link_to_university', 'verified', 'active')
    search_fields = ('user__username', 'name', 'requested_university__name',
                     'requested_university__abbreviation')

    def email(self, obj):
        """Returns manager's email"""
        return obj.user.email

    def verified(self, obj):
        """Returns manager verification status"""
        return True if obj.requested_university.user == obj.user else False

    verified.boolean = True
    verified.admin_order_field = 'requested_university__user'

    def active(self, obj):
        """Returns manager activation status"""
        return obj.user.is_active

    active.boolean = True
    active.admin_order_field = 'user__is_active'

    def link_to_university(self, obj):
        """Returns a link to manager's requested university"""
        link = urlresolvers.reverse('admin:participant_university_change',
                                    args=[obj.requested_university.id])
        return format_html('<a href="{}">{}</a>', link, obj.requested_university.name)

    link_to_university.short_description = 'Universitas'



@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'division', 'core_member_count', 'mechanics_count',
                    'adviser_count', 'is_complete')
    list_filter = ('university', 'division')
    search_fields = ('name', 'university__name', 'university__abbreviation')

    def core_member_count(self, obj):
        """Returns the team's core member count"""
        return obj.core_member().count()

    def mechanics_count(self, obj):
        """Returns the team's mechanics count"""
        return obj.mechanics().count()

    def adviser_count(self, obj):
        """Returns the team's adviser count"""
        return obj.adviser().count()


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_name', 'university', 'type', 'gender', 'is_complete')
    list_filter = ('type', 'gender')
    search_fields = ('name', 'team__name', 'team__university__name',
                     'team__university__abbreviation')

    def team_name(self, obj):
        """Returns the person's team name"""
        return obj.team.name

    team_name.admin_order_field = 'team__name'
    team_name.short_description = 'Team'

    def university(self, obj):
        """Returns the person's university name"""
        return obj.team.university.name

    university.admin_order_field = 'team__university__name'

