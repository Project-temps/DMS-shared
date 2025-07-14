import pandas as pd
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from unittest.mock import patch

from .views import PredictionAPIView

class CalculateTHIAPITestCase(APITestCase):
    @patch('api.views.calculate_thi')
    def test_calculate_thi_api(self, mock_calculate):
        df_de = pd.DataFrame([{"datetime": "2024-01-01T00:00:00", "thi": 50}])
        df_pl = pd.DataFrame([{"datetime": "2024-01-01T00:00:00", "thi": 40}])
        mock_calculate.return_value = (df_de, df_pl)
        url = reverse('calculate-thi-api')
        response = self.client.get(url)
        expected = {
            'Germany': df_de.to_dict(orient='records'),
            'Poland': df_pl.to_dict(orient='records'),
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)

class PredictionAPITestCase(APITestCase):
    @patch('api.views.make_prediction')
    def test_prediction_api(self, mock_prediction):
        mock_prediction.return_value = 123
        factory = APIRequestFactory()
        view = PredictionAPIView.as_view()
        request = factory.post('/dummy/', {'foo': 'bar'}, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'prediction': 123})
        mock_prediction.assert_called_once_with({'foo': 'bar'})
