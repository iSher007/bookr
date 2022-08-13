from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from django.test import TestCase, Client
from bookr_test.models import *
from bookr_test.views import greeting_view


class TestModelClass(TestCase):
    def setUp(self):
        self.p = Publisher(name='Packt', website='www.packt.com', email='contact@packt.com')

    def test_create_publisher(self):
        self.assertIsInstance(self.p, Publisher)

    def test_str_representation(self):
        self.assertEquals(str(self.p), "Packt")


class TestGreetingView(TestCase):
    """Test the greeting view."""

    def setUp(self):
        self.client = Client()

    def test_greeting_view(self):
        response = self.client.get('/test/')
        self.assertEquals(response.status_code, 200)


class TestLoggedInGreetingView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='test@#628password')
        self.test_user.save()
        self.factory = RequestFactory()
        self.client = Client()

    def test_user_greeting_not_authenticated(self):
        request = self.factory.get('/test/')
        request.user = AnonymousUser()
        response = greeting_view(request)
        self.assertEquals(response.status_code, 302)

    def test_user_authenticated(self):
        request = self.factory.get('/test/')
        request.user = self.test_user
        response = greeting_view(request)
        self.assertEquals(response.status_code, 200)
