from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile

class ProfileModelTests(TestCase):
    def test_str_representation(self):
        user = User.objects.create(username='john')
        profile = Profile.objects.create(user=user, group='farmer')
        self.assertEqual(str(profile), 'john (farmer)')

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='secret', is_active=True)

    def test_login_success_redirects(self):
        client = Client()
        response = client.post('/auth/login/', {'username': 'alice', 'password': 'secret'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')
        self.assertEqual(int(client.session['_auth_user_id']), self.user.id)
