from django.urls import path
from . import views

app_name = 'app_search'

urlpatterns = [
    path("", views.index, name='search')
]
