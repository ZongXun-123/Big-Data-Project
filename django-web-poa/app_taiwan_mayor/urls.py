from django.urls import path
from app_taiwan_mayor import views

app_name='app_taiwan_mayor'

urlpatterns = [
    path('', views.home, name='home'),
    path('api_get_taiwan_mayor_data/', views.api_get_taiwan_mayor_data),
]
