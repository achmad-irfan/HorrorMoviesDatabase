from django.contrib import admin
from django.urls import path,include
from . import views


app_name='app_hgraphy'
urlpatterns = [
    path("",views.index,name='hgraphy'),
]