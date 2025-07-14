from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('allerts/', views.allerts, name='allerts'),
    path('contact/', views.contact, name='contact'),
    path('survey/', views.survey, name='survey'),
    path('communication/', views.communication, name='communication'),
    path('api/getChartData', views.get_chart_data, name='get_chart_data'),
    path('api/get_thi_data/', views.get_thi_data, name='get_thi_data'),

]
