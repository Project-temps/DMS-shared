from django.test import TestCase, RequestFactory
import json
from .views import process_data

class ProcessDataViewTests(TestCase):
    def test_process_data_returns_success(self):
        factory = RequestFactory()
        request = factory.get('/process/')
        response = process_data(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'Data processed successfully'})
