from django.test import TestCase
from django.contrib.auth.models import User
from kri.apps.participant.tests import TeamTestCase, PersonTestCase
from .models import Card, CardLog

class CardTestCase(TestCase):
    def setUp(self):
        team = TeamTestCase.mock_team('SPY', 'krai')
        person = PersonTestCase.mock_person('John Doe', team, 'core_member')
        self.card = Card.register(person.id, 'key')

    def test_card_registration(self):
        """Test card registration"""
        self.assertEqual(self.card.person.name, 'John Doe')

    def test_status(self):
        """Test card status"""
        self.assertEqual(self.card.logged_in(), False)

    def test_card_login(self):
        """Test normal login"""
        self.card.login()
        self.assertEqual(self.card.logged_in(), True)

    def test_card_login_while_inside(self):
        """Test login when the card is inside"""
        self.card.login()
        status = self.card.login()

        self.assertEqual(status, False)
        self.assertEqual(self.card.logged_in(), True)

    def test_card_logout(self):
        """Test normal logout"""
        self.card.login()
        self.card.logout()

        self.assertEqual(self.card.logged_in(), False)

    def test_card_logout_while_outside(self):
        """Test logout when the card is outside"""
        self.card.logout()

        self.assertEqual(self.card.logged_in(), False)


class CardLogTestCase(TestCase):
    def setUp(self):
        team = TeamTestCase.mock_team('SPY', 'krai')
        person = PersonTestCase.mock_person('John Doe', team, 'core_member')
        self.card = Card.register(person.id, 'key')
        self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'password')

    def test_invalid_card_key(self):
        """Invalid card key should raise Card.DoesNotExist"""
        with self.assertRaises(Card.DoesNotExist):
            log = CardLog.login('invalid key', self.admin)

    def test_login(self):
        """Test normal login"""
        log = CardLog.login(self.card.key, self.admin)

        self.assertEqual(log.activity, 'login')

    def test_duplicate_login(self):
        """Test login when the Card is inside"""
        CardLog.login(self.card.key, self.admin)
        log = CardLog.login(self.card.key, self.admin)

        self.assertEqual(log, None)

    def test_logout(self):
        """Test normal logout"""
        CardLog.login(self.card.key, self.admin)
        log = CardLog.logout(self.card.key, self.admin)

        self.assertEqual(log.activity, 'logout')

    def test_duplicate_logout(self):
        """Test logout when the Card is outside"""
        CardLog.login(self.card.key, self.admin)
        CardLog.logout(self.card.key, self.admin)
        log = CardLog.logout(self.card.key, self.admin)

        self.assertEqual(log, None)

    def test_last_by_admin(self):
        """Test last_by_admin to get the latest CardLog by an admin"""
        CardLog.login(self.card.key, self.admin)
        CardLog.logout(self.card.key, self.admin)
        log = CardLog.login(self.card.key, self.admin)

        self.assertEqual(CardLog.last_by_admin(self.admin).time, log.time)
