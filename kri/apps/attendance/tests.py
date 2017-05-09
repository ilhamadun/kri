import json
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from kri.apps.participant.tests import TeamTestCase, PersonTestCase
from .models import Card, CardLog
from .views import fetch_log, login, logout

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

        self.assertEqual(log.activity, 'login_granted')

    def test_duplicate_login(self):
        """Test login when the Card is inside"""
        CardLog.login(self.card.key, self.admin)
        log = CardLog.login(self.card.key, self.admin)

        self.assertEqual(log.activity, 'login_denied')

    def test_logout(self):
        """Test normal logout"""
        CardLog.login(self.card.key, self.admin)
        log = CardLog.logout(self.card.key, self.admin)

        self.assertEqual(log.activity, 'logout_granted')

    def test_duplicate_logout(self):
        """Test logout when the Card is outside"""
        CardLog.login(self.card.key, self.admin)
        CardLog.logout(self.card.key, self.admin)
        log = CardLog.logout(self.card.key, self.admin)

        self.assertEqual(log.activity, 'logout_denied')

    def test_last_by_admin(self):
        """Test last_by_admin to get the latest CardLog by an admin"""
        CardLog.login(self.card.key, self.admin)
        CardLog.logout(self.card.key, self.admin)
        log = CardLog.login(self.card.key, self.admin)

        self.assertEqual(CardLog.last_by_admin(self.admin).time, log.time)

    def test_request_login(self):
        """Requests a normal login"""
        factory = RequestFactory()
        request = factory.post('/attendance/login/', {
            'card_key': self.card.key,
        })
        request.user = self.admin
        response = login(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads((response.content).decode('utf-8'))
        self.assertEqual(data['activity'], 'login')
        self.assertEqual(data['message'], 'Login granted.')
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['person']['name'], self.card.person.name)

    def test_request_login_invalid_key(self):
        """Requests login with invalid key"""
        factory = RequestFactory()
        request = factory.post('/attendance/login/', {
            'card_key': 'invalidkey',
        })
        request.user = self.admin
        response = login(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads((response.content).decode('utf-8'))
        self.assertEqual(data['activity'], 'login')
        self.assertEqual(data['message'], 'Card not recognized.')
        self.assertEqual(data['status'], 'failed')

    def test_request_duplicate_login(self):
        """Requests a duplicate login"""
        factory = RequestFactory()
        request = factory.post('/attendance/login/', {
            'card_key': self.card.key,
        })
        request.user = self.admin
        response = login(request)
        response = login(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads((response.content).decode('utf-8'))
        self.assertEqual(data['activity'], 'login')
        self.assertEqual(data['message'], 'Login denied.')
        self.assertEqual(data['status'], 'denied')

    def test_request_logout(self):
        """Requests a normal logout"""
        factory = RequestFactory()
        request = factory.post('/attendance/logout/', {
            'card_key': self.card.key,
        })
        request.user = self.admin
        response = login(request)
        response = logout(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads((response.content).decode('utf-8'))
        self.assertEqual(data['activity'], 'logout')
        self.assertEqual(data['message'], 'Logout granted.')
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['person']['name'], self.card.person.name)

    def test_request_logout_invalid_key(self):
        """Requests logout with invalid key"""
        factory = RequestFactory()
        request = factory.post('/attendance/logout/', {
            'card_key': 'invalidkey',
        })
        request.user = self.admin
        response = logout(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads((response.content).decode('utf-8'))
        self.assertEqual(data['activity'], 'logout')
        self.assertEqual(data['message'], 'Card not recognized.')
        self.assertEqual(data['status'], 'failed')

    def test_request_duplicate_logout(self):
        """Requests a duplicate logout"""
        factory = RequestFactory()
        request = factory.post('/attendance/logout/', {
            'card_key': self.card.key,
        })
        request.user = self.admin
        response = login(request)
        response = logout(request)
        response = logout(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads((response.content).decode('utf-8'))
        self.assertEqual(data['activity'], 'logout')
        self.assertEqual(data['message'], 'Logout denied.')
        self.assertEqual(data['status'], 'denied')

    def test_request_log(self):
        factory = RequestFactory()
        request = factory.post('/attendance/logout/', {
            'card_key': self.card.key,
        })
        request.user = self.admin
        response = login(request)

        request = factory.get('/attendance/fetch-log')
        request.user = self.admin
        response = fetch_log(request)

        self.assertEqual(response.status_code, 200)
        data = json.loads((response.content).decode('utf-8'))
        self.assertEqual(data['status'], 'login_granted')
        self.assertEqual(data['person']['name'], self.card.person.name)

        request = factory.post('/attendance/logout/', {
            'card_key': self.card.key,
        })
        request.user = self.admin
        login_response = login(request)

        response = fetch_log(request)
        data = json.loads((login_response.content).decode('utf-8'))

        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(data['status'], 'denied')

    def test_request_log_no_content(self):
        factory = RequestFactory()
        request = factory.get('/attendance/fetch-log')
        request.user = self.admin
        response = fetch_log(request)

        self.assertEqual(response.status_code, 204)
