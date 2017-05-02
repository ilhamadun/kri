from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import University, Manager, Team, Person, Supporter

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
    link_to_manager.admin_order_field = 'user__manager__name'


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'email', 'link_to_university', 'verified', 'active')
    readonly_fields = ('email', 'verified', 'active')
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
    readonly_fields = ('core_member', 'mechanics', 'adviser')
    search_fields = ('name', 'university__name', 'university__abbreviation')

    def core_member(self, obj):
        return self.create_person_link(obj.core_member())

    def mechanics(self, obj):
        return self.create_person_link(obj.mechanics())

    def adviser(self, obj):
        return self.create_person_link(obj.adviser())

    def create_person_link(self, persons):
        text = '<br/><ol>'
        for m in persons:
            link = urlresolvers.reverse('admin:participant_person_change',
                                        args=[m.id])
            text = text + format_html('<li><a href="{}">{}</a> ({})</li>', link, m.name,
                                      'Lengkap' if m.is_complete() else 'Belum Lengkap')

        text = text + '</ol>'

        return mark_safe(text)

    def core_member_count(self, obj):
        """Returns the team's core member count"""
        return obj.core_member().count()

    def mechanics_count(self, obj):
        """Returns the team's mechanics count"""
        return obj.mechanics().count()

    def adviser_count(self, obj):
        """Returns the team's adviser count"""
        return obj.adviser().count()

    core_member_count.short_description = 'Core Member'
    mechanics_count.short_description = 'Mechanics'
    adviser_count.short_description = 'Adviser'


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


@admin.register(Supporter)
class SupporterAdmin(admin.ModelAdmin):
    list_display = ('university', 'amount', 'price', 'is_active', 'order_time',
                    'verification_button')
    search_fields = ('user__university__name', 'user__university__abbreviation')

    def university(self, obj):
        """Return university name"""
        return obj.user.university.name

    def is_active(self, obj):
        """Return whether ticket order is active or not"""
        return not obj.is_obselete()

    is_active.short_description = 'Active'
    is_active.boolean = True

    def verification_button(self, obj):
        """Returns a unique verification link for each ticket"""
        if obj.verified_time is not None:
            return obj.verified_time

        if not obj.is_obselete():
            verify_link = urlresolvers.reverse('participant:verify-supporter', args=[obj.id])
            next_link = urlresolvers.reverse('admin:participant_supporter_changelist')

            button = '<a href="{0}?next={1}" class="link">Verifikasi</a>'.format(verify_link,
                                                                                 next_link)

            return mark_safe(button)
        else:
            return '-'

    verification_button.short_description = 'Verify'
