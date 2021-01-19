from stock import views
from django.urls import path, include

#app_name='stock'

urlpatterns = [
    path('', views.main, name='main'),
]