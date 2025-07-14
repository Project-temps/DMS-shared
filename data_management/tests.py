from django.test import TestCase, RequestFactory
import json
from .views import collect_data

class CollectDataViewTests(TestCase):
    def test_collect_data_returns_success(self):
        factory = RequestFactory()
        request = factory.get('/collect/')
        response = collect_data(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'Data collected successfully'})
