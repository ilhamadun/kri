"""Participant

The participant app consist of three related models: University, Team and Person.
Each University has multiple Team and each Team has multiple Person.

"""

import datetime
import hashlib
import random
from django.db import models, IntegrityError
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone


class University(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, null=True)
    user = models.OneToOneField(User, models.CASCADE, blank=True, null=True)
    krai = models.BooleanField(default=False)
    krsbi_beroda = models.BooleanField(default=False)
    krsti = models.BooleanField(default=False)
    krpai = models.BooleanField(default=False)

    def has_access(self, division):
        """Check if the university could participate in a division

        Args:
            - division: the division to check

        Returns:
            - boolean, the privileges to participate

        Raises:
            - AssertionError: division is not a member of TEAM_DIVISION

        """
        assert division in ('krai', 'krsbi_beroda', 'krsti', 'krpai', 'pers'), (
            'division is not a member of TEAM_DIVISION.')

        if division == 'pers':
            return True

        return bool(getattr(self, division))

    def all_access(self):
        """List the university's privileges on each division"""
        access = {}
        for division in Team.TEAM_DIVISION:
            access[division[0]] = self.has_access(division[0])

        return access

    def team(self, division):
        """Get the university's team for the division

        Raises:
            ObjectDoesNotExist: no team exist for the division
        """
        try:
            return Team.objects.from_university(self, division)
        except ObjectDoesNotExist:
            raise

    def __str__(self):
        return self.name

    def is_complete(self):
        """Check if university data is complete, including team and person data"""
        if list(self.all_access().values()).count(True) != self.teams.count():
            return False

        for t in self.teams.all():
            if not t.is_complete():
                return False

        return True

    is_complete.boolean = True
    is_complete.short_description = 'Complete'

    class Meta:
        verbose_name_plural = 'Universities'


def manager_image_directory(instance, filename):
    """Generate a unique image upload path for each manager"""
    salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5]
    return 'manager/{0}/{1}'.format(instance.requested_university.id, salt + '_' + filename)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15)
    requested_university = models.ForeignKey(University, on_delete=models.CASCADE)
    student_card = models.ImageField(upload_to=manager_image_directory, null=True, default=None)

    def __str__(self):
        return self.user.username


class TeamManager(models.Manager):
    """Object manager for the Team model"""
    def create(self, **kwargs):
        """Create a new Team

        A team could only be created if two conditions are met:
            - the university has a privileges to enter the competition
            - A university could only have one team for each division

        If those condition are not met, an exception is raised.

        Returns:
            - New Team instance

        Raises:
            - IntegrityError: the university tries to create more than one team for a division
            - PermissionDenied: the university has no previleges to participate on the division

        """
        university = kwargs['university']
        division = kwargs['division']

        if university.has_access(division):
            if self.exists(university, division):
                raise IntegrityError('{0} sudah memiliki tim {1}.'.format(
                    university.name, Team.division_type_display(division)))

            team = self.model(**kwargs)
            team.save()

            return team
        else:
            raise PermissionDenied('{0} tidak mengikuti {1}.'.format(
                university.name, Team.division_type_display(division)))

    def exists(self, university, division):
        """Check if the university has a team for the division"""
        try:
            return bool(self.from_university(university, division))
        except ObjectDoesNotExist:
            return False

    def from_university(self, university, division=None):
        """Fetch the university's team

        Returns:
            - If division is provided, returns a single team on the division.
              Otherwise returns a list of team.

        Raises:
            - DoesNotExist: no team exist for the division

        """
        teams = super(TeamManager, self).filter(university=university)
        if division:
            try:
                teams = teams.get(division=division)
            except ObjectDoesNotExist:
                raise

        return teams


def team_image_directory(instance, filename):
    """Generate a unique image upload path for each team"""
    salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5]
    return 'team/{0}/{1}'.format(instance.id, salt + '_' + filename)


class Team(models.Model):
    TEAM_DIVISION = (
        ('krai', 'KRAI'),
        ('krsbi_beroda', 'KRSBI Beroda'),
        ('krsti', 'KRSTI'),
        ('krpai', 'KRPAI'),
        ('pers', 'PERS')
    )

    MAX_CORE_MEMBER = {'krai': 3, 'krsbi_beroda': 4, 'krsti': 3, 'krpai': 2}
    MAX_MECHANIC = {'krai': 3, 'krsbi_beroda': 1, 'krsti': 1, 'krpai': 1}
    MAX_PERS = {'krai': 0, 'krsbi_beroda': 0, 'krsti': 0, 'krpai': 0, 'pers': 1}

    name = models.CharField(max_length=100, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='teams')
    division = models.CharField(max_length=12, choices=TEAM_DIVISION)
    arrival_time = models.DateTimeField(null=True)
    transport = models.CharField(max_length=100, null=True)
    objects = TeamManager()

    def max_core_member(self):
        """Returns the maximum core member allowed for the team"""
        return self.MAX_CORE_MEMBER[self.division]

    def max_mechanics(self):
        """Returns the maximum mechanics allowed for the team"""
        return self.MAX_MECHANIC[self.division]

    def max_adviser(self):
        """Returns the maximum adviser allowed for the team"""
        return 1

    def max_pers(self):
        """Returns the maximum pers allowed for the team"""
        return self.MAX_PERS[self.division]

    def core_member(self):
        """Returns list of the team's core member"""
        return self.persons.filter(type='core_member')

    def mechanics(self):
        """Returns list of the team's mechanics"""
        return self.persons.filter(type='mechanics')

    def adviser(self):
        """Returns list of the team's adviser"""
        return self.persons.filter(type='adviser')

    def pers(self):
        """Returns list of the team's pers"""
        return self.persons.filter(type='pers')

    def available_slot(self, person_type):
        """Get available slot for a person type"""
        return getattr(self, 'max_' + person_type)() - getattr(self, person_type)().count()

    def __str__(self):
        return self.name + ' - ' + self.university.name

    def is_complete(self):
        """Check if team data is complete, including person data"""
        if not self.name and self.arrival_time and self.transport:
            return False

        if not (self.core_member() and self.adviser()):
            return False

        for m in self.persons.all():
            if not m.is_complete():
                return False

        return True

    is_complete.boolean = True
    is_complete.short_description = 'Complete'

    @staticmethod
    def division_type_display(key):
        """Returns display value from TEAM_DIVISION"""
        for d in Team.TEAM_DIVISION:
            if d[0] == key:
                return d[1]

        return None


def person_image_directory(instance, filename):
    """Generate a unique image upload path for each person"""
    salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5]
    return 'person/{0}/{1}'.format(instance.id, salt + '_' + filename)


class PersonManager(models.Manager):
    """Object manager for the Person model"""
    def create(self, **kwargs):
        """Create a new Person

        The Person will only be created if the team member is still below the maximum
        number of person for each person type.

        Returns:
            - New Person instance

        Raises:
            - IntegrityError: attempted to create a person over the person type's limit

        """
        team = kwargs['team']
        person_type = kwargs['type']

        member_count = getattr(team, person_type)().count()
        max_member = getattr(team, 'max_' + person_type)()

        if member_count < max_member:
            person = self.model(**kwargs)
            person.save()

            return person
        else:
            raise IntegrityError('{0} tim {1} sudah penuh.'.format(
                Person.person_type_display(person_type), team.name))


class Person(models.Model):
    PERSON_TYPE = (
        ('core_member', 'Tim Inti'),
        ('mechanics', 'Mekanik'),
        ('adviser', 'Dosen Pembimbing'),
        ('supporter', 'Supporter'),
        ('pers', 'PERS')
    )

    GENDER = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan')
    )

    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='persons')
    type = models.CharField(max_length=11, choices=PERSON_TYPE)
    instance_id = models.CharField(max_length=30)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    photo = models.ImageField(upload_to=person_image_directory, blank=True)
    objects = PersonManager()

    def __str__(self):
        return self.name

    def is_complete(self):
        """Check if person data is complete"""
        if self.photo:
            return True
        else:
            return False

    is_complete.boolean = True
    is_complete.short_description = 'Complete'

    @staticmethod
    def person_type_display(key):
        """Returns display value from PERSON_TYPE"""
        for p in Person.PERSON_TYPE:
            if p[0] == key:
                return p[1]

        return None


class Supporter(models.Model):
    MAX_TICKET = 600
    MAX_SUPPORTER = 40
    PRICE = 25000

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supporter')
    amount = models.IntegerField()
    price = models.IntegerField()
    order_time = models.DateTimeField(auto_now_add=True)
    verification_time = models.DateTimeField(null=True)
    verified_time = models.DateTimeField(null=True)

    def is_obselete(self):
        """Check if an order is obselete

        Every order is obselete in 24 hours.
        """
        delta = timezone.now() - self.order_time

        if delta.days >= 1:
            return True
        else:
            return False

    @staticmethod
    def max_supporter(university):
        """Get maximum supporter for a university"""
        if university.name == 'Universitas Gadjah Mada':
            supporter = 100
        else:
            supporter = Supporter.MAX_SUPPORTER

        return supporter

    @staticmethod
    def tickets_left(user=None):
        """Get ticket left for all or for a user

        Args:
            - user: user to check

        """
        now = timezone.now()
        yesterday = now - datetime.timedelta(1)

        tickets = Supporter.objects.filter(
            models.Q(verified_time__isnull=False) |
            # models.Q(verification_time__isnull=False) |
            models.Q(order_time__gte=yesterday)
        )

        if user:
            global_ticket_sum = tickets.aggregate(models.Sum('amount'))['amount__sum']

            tickets = tickets.filter(user=user)
            max_supporter = Supporter.max_supporter(user.university)

            if global_ticket_sum is not None:
                global_ticket_left = Supporter.MAX_TICKET - global_ticket_sum

                if max_supporter >= global_ticket_left:
                    return global_ticket_left
        else:
            max_supporter = Supporter.MAX_TICKET

        tickets = tickets.aggregate(models.Sum('amount'))

        if tickets['amount__sum'] is None:
            return max_supporter
        else:
            return max_supporter - tickets['amount__sum']

    @staticmethod
    def order(form, user):
        """Order tickets for user from SupporterForm

        Args:
            - form: instance of SupporterForm
            - user: order's user

        Return:
            The ticket, if order is succeed, or None if it failed

        """
        tickets_left = Supporter.tickets_left(user)
        if form.is_valid() and int(form.data['amount']) <= tickets_left:
            ticket = form.save(commit=False)
            ticket.user = user
            ticket.price = int(form.cleaned_data['amount']) * Supporter.PRICE
            ticket.save()

            return ticket
        else:
            return None

    @staticmethod
    def verify(ticket_id):
        """Verifiy ticket order"""
        ticket = Supporter.objects.get(pk=ticket_id)
        now = timezone.now()
        ticket.verification_time = now
        ticket.verified_time = now
        ticket.save()

    @staticmethod
    def price_due(user):
        """Count price due for a user"""
        now = timezone.now()
        yesterday = now - datetime.timedelta(1)
        orders = Supporter.objects.filter(user=user).filter(order_time__gte=yesterday)
        price = 0
        for order in orders:
            if not order.verified_time:
                price = price + order.price

        return price

    @staticmethod
    def ticket_ordered(user):
        """Count number of ticket ordered for a user"""
        return Supporter.max_supporter(user.university) - Supporter.tickets_left(user)
 