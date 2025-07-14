from django.urls import path
from . import views

urlpatterns = [
    path('collect/', views.collect_data, name='collect_data'),
]
