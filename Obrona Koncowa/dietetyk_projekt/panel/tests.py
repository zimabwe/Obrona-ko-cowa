from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
class RegisterPacjentViewTest(TestCase):

    def test_register_pacjent_view(self):
        url = reverse('rejestracja')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'id="id_username"')
        self.assertContains(response, 'id="id_email"')
        self.assertContains(response, 'id="id_password1"')
        self.assertContains(response, 'id="id_password2"')

    def test_register_pacjent_submission(self):
        url = reverse('rejestracja')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(url, data)


        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

class LoginPacjentViewTest(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
        )

    def test_login_pacjent_view(self):
        url = reverse('login')
        response = self.client.get(url)


        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'id="id_username"')
        self.assertContains(response, 'id="id_password"')

    def test_login_pacjent_valid_submission(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123',
        }
        response = self.client.post(url, data)


        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('panel_pacjenta'))

    def test_login_pacjent_valid_staff_submission(self):
        staff_user = get_user_model().objects.create_user(
            username='staffuser',
            email='staffuser@example.com',
            password='staffpass123',
            is_staff=True,
        )

        url = reverse('login')
        data = {
            'username': 'staffuser',
            'password': 'staffpass123',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('panel_dietetyka'))