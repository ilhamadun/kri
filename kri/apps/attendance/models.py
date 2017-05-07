from django.db import models
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.auth.models import User
from kri.apps.participant.models import Person


class Card(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    register_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    def login(self):
        """Log the card in

        Any card can only be logged in if it's status is logged out. Attempt to login while
        it's logged in will be ignored.

        Returns:
            True if login is success, otherwise False

        """
        if not self.logged_in():
            self.last_login = timezone.now()
            self.save()

            return True

        return False

    def logout(self):
        """Log the card out

        Any card can only be logged out if it's status is logged in. Attempt to logout while
        it's logged out will be ignored.

        Returns:
            True if logout is success, otherwise False

        """
        if self.logged_in():
            self.last_logout = timezone.now()
            self.save()

            return True

        return False

    def logged_in(self):
        """Check card status

        Returns:
            Whether the card's status is logged in or logged out.

        """
        if self.last_login is not None:
            if self.last_logout is None or self.last_login > self.last_logout:
                return True

        return False

    @staticmethod
    def register(person_id, key):
        """Register Person to a card"""
        person = Person.objects.get(pk=person_id)

        return Card.objects.create(person=person, key=key)


class CardLog(models.Model):
    ACTIVITY = (
        ('login_granted', 'Log In Granted'),
        ('login_denied', 'Log In Denied'),
        ('logout_granted', 'Log Out Granted'),
        ('logout_denied', 'Log Out Denied')
    )

    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=15, choices=ACTIVITY)
    time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def login(card_key, admin):
        """Log the card in

        Returns:
            The CardLog object

        """
        return CardLog.create_log(card_key, 'login', admin)

    @staticmethod
    def logout(card_key, admin):
        """Log the card in

        Returns:
            The CardLog object

        """
        return CardLog.create_log(card_key, 'logout', admin)

    @staticmethod
    def create_log(card_key, activity, admin):
        """Create an activity log

        Returns:
            The CardLog object

        """
        assert activity in ['login', 'logout']

        if not admin.has_perm('attendance.add_card_log'):
            raise PermissionDenied

        try:
            card = Card.objects.get(key=card_key)
        except Card.DoesNotExist:
            raise
        else:
            if getattr(card, activity)():
                log_activity = activity + '_granted'
            else:
                log_activity = activity + '_denied'

            return CardLog.objects.create(card=card, admin=admin, activity=log_activity)

        return None

    @staticmethod
    def last_by_admin(admin):
        """Get the latest CardLog created by the admin"""
        try:
            return CardLog.objects.filter(admin=admin).order_by('-time')[0]
        except IndexError:
            return None
