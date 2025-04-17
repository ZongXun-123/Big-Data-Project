from django.urls import path
from app_top_keyword import views

app_name = 'app_top_keyword'

urlpatterns = [
    # For home
    path('', views.home, name='home'),
    # For Ajax
    path('api_get_cate_topword/', views.api_get_cate_topword, name='api_cate_topword'),
]
