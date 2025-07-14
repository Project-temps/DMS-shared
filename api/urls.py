from django.urls import path
from .views import CalculateTHIAPIView


urlpatterns = [
    path('calculate_thi/', CalculateTHIAPIView.as_view(), name='calculate-thi-api'),
]
