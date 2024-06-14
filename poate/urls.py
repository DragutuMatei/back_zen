# urls.py

from django.urls import path
from .views import create_data

urlpatterns = [
    path('create_data/', create_data, name='create_data'),
    # Add other URLs as needed
]
