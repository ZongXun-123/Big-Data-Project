"""website_configs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from turtle import home
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('topword/', include('app_top_keyword.urls')),
    path('topperson/', include('app_top_person.urls')),
    path('userkeyword/', include('app_user_keyword.urls')),
    path('keyperson/', include('app_key_person.urls')),
    path('userkeyword_assoc/', include('app_user_keyword_association.urls')),
    path('userkeyword_senti/', include('app_user_keyword_sentiment.urls')),
    path('taiwanmayor/', include('app_taiwan_mayor.urls')),
    path('userkeyword_db/', include('app_user_keyword_db.urls')),
    path('topperson_db/', include('app_top_person_db.urls')),
    path('admin/', admin.site.urls),
    path('', include('app_top_keyword.urls')),
    path('', include('app_top_person.urls')),
    path('', include('app_user_keyword.urls')),
    path('', include('app_key_person.urls')),
    path('', include('app_user_keyword_association.urls')),
    path('', include('app_user_keyword_sentiment.urls')),
    path('', include('app_taiwan_mayor.urls')),
    path('', include('app_user_keyword_db.urls')),
    path('', include('app_top_person_db.urls')),
    path('', home),
]
