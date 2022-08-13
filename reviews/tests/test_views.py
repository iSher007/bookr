from django.test import TestCase, Client, RequestFactory
from reviews.views import index


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_index(self):
        request = self.factory.get('')
        request.session = {}
        response = index(request)
        self.assertEquals(response.status_code, 200)
