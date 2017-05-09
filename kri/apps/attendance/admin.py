from django.contrib import admin
from .models import Card, CardLog


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('person', 'key', 'last_login', 'last_logout')


@admin.register(CardLog)
class CardLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'activity', 'time')

    def name(self, obj):
        return obj.card.person.name
