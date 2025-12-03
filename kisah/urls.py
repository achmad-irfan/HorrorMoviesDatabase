from django.urls import path
from . import views

app_name = 'app_kisah'

urlpatterns = [
    path("", views.index, name='kisah')
]
