"""Test cases for participant application"""

import datetime
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.test import TestCase
from . import models


class UniversityTestCase(TestCase):
    """Test cases for University model"""
    @staticmethod
    def mock_university():
        """Create a University instance for testing purpose"""
        return models.University.objects.create(
            name='Universitas Gadjah Mada',
            abbreviation='UGM',
            krai=True,
            krsbi_beroda=False,
            krsti=True,
            krpai=False
        )

    def setUp(self):
        self.university = UniversityTestCase.mock_university()

    def test_division_access(self):
        """Test the university's privileges on a division"""
        self.assertTrue(self.university.has_access(0))
        self.assertFalse(self.university.has_access(1))
        self.assertTrue(self.university.has_access(2))
        self.assertFalse(self.university.has_access(3))


class TeamTestCase(TestCase):
    """Test cases for Team model"""
    @staticmethod
    def mock_team(name, division, university=None):
        """Create a Team instance for testing purpose"""
        if university is None:
            university = UniversityTestCase.mock_university()

        return models.Team.objects.create(
            name=name,
            university=university,
            division=division
        )

    def setUp(self):
        self.university = UniversityTestCase.mock_university()

    def test_create_team(self):
        """Test a successful team creation"""
        DIVISION = 0

        TeamTestCase.mock_team('KRPAI', DIVISION, self.university)
        team = models.Team.objects.get(name='KRPAI')

        self.assertEqual(team.university.name, self.university.name)
        self.assertEqual(team.max_core_member(), models.Team.MAX_CORE_MEMBER[DIVISION])
        self.assertEqual(team.max_mechanics(), models.Team.MAX_MECHANIC[DIVISION])
        self.assertEqual(team.max_adviser(), 1)

    def test_create_team_premission_denied(self):
        """Test team creation on university with no privileges"""
        with self.assertRaises(PermissionDenied) as error:
            TeamTestCase.mock_team('KRSBI Beroda', 1, self.university)

        self.assertEqual(error.exception.args[0],
                         'Universitas Gadjah Mada tidak mengikuti KRSBI Beroda.')

    def test_create_duplicate_team(self):
        """Test tean creation when the university has another team on the same division"""
        TeamTestCase.mock_team('KRSTI', 2, self.university)

        with self.assertRaises(IntegrityError) as error:
            TeamTestCase.mock_team('KRSTI', 2, self.university)

        self.assertEqual(error.exception.args[0],
                         'Universitas Gadjah Mada sudah memiliki tim KRSTI.')

    def test_create_team_invalid_division(self):
        """Test team creation with invalid division"""
        with self.assertRaises(AssertionError) as error:
            TeamTestCase.mock_team('Team', 4, self.university)

        self.assertEqual(error.exception.args[0],
                         'division is not a member of TEAM_DIVISION.')

    def test_team_max_member(self):
        """Test the Team maximum number of member"""
        university = UniversityTestCase.mock_university()
        team = TeamTestCase.mock_team('KRPAI', 2, university)

        for i in range(team.max_core_member()):
            PersonTestCase.mock_person('core-{0}'.format(i), team, 'core_member')

        for i in range(team.max_mechanics()):
            PersonTestCase.mock_person('mechanics-{0}'.format(i), team, 'mechanics')

        for i in range(team.max_adviser()):
            PersonTestCase.mock_person('adviser-{0}'.format(i), team, 'adviser')

        team.refresh_from_db()

        self.assertEqual(team.core_member().count(), team.max_core_member())
        self.assertEqual(team.mechanics().count(), team.max_mechanics())
        self.assertEqual(team.adviser().count(), team.max_adviser())

class PersonTestCase(TestCase):
    """Test cases for Person model"""
    @staticmethod
    def mock_person(name, team, person_type):
        """Create a Person instance for testing purpose"""
        return models.Person.objects.create(
            name=name,
            team=team,
            type=person_type,
            instance_id='instanceid',
            birthday=datetime.datetime.now(),
            gender='L',
            phone='081234567890',
            email='email@test.com',
            shirt_size='l'
        )

    def setUp(self):
        self.university = UniversityTestCase.mock_university()
        self.university.krpai = True
        self.university.save()
        self.team = TeamTestCase.mock_team('KRPAI', 3, self.university)

    def test_create_person(self):
        """Test person creation"""
        person = PersonTestCase.mock_person('John Doe', self.team, 'core_member')

        self.assertEqual(person.team.university.name, 'Universitas Gadjah Mada')

    def test_over_core_member(self):
        """Test person creation exceeding maximum core_member"""
        for i in range(self.team.max_core_member()):
            PersonTestCase.mock_person('core-{0}'.format(i), self.team, 'core_member')

        with self.assertRaises(IntegrityError) as error:
            PersonTestCase.mock_person('core-{0}'.format(self.team.max_core_member()),
                                       self.team, 'core_member')

        self.assertEqual(error.exception.args[0],
                         'Tim Inti tim KRPAI sudah penuh.')

    def test_over_mechanics(self):
        """Test person creation exceeding maximum mechanics"""
        for i in range(self.team.max_mechanics()):
            PersonTestCase.mock_person('mechanics-{0}'.format(i), self.team, 'mechanics')

        with self.assertRaises(IntegrityError) as error:
            PersonTestCase.mock_person('mechanics-{0}'.format(self.team.max_mechanics()),
                                       self.team, 'mechanics')

        self.assertEqual(error.exception.args[0],
                         'Mekanik tim KRPAI sudah penuh.')

    def test_over_adviser(self):
        """Test person creation exceeding maximum adviser"""
        for i in range(self.team.max_adviser()):
            PersonTestCase.mock_person('adviser-{0}'.format(i), self.team, 'adviser')

        with self.assertRaises(IntegrityError) as error:
            PersonTestCase.mock_person('adviser-{0}'.format(self.team.max_adviser()),
                                       self.team, 'adviser')

        self.assertEqual(error.exception.args[0],
                         'Dosen Pembimbing tim KRPAI sudah penuh.')
