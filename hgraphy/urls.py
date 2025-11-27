from django.contrib import admin
from django.urls import path,include
from . import views


app_name='app_hgraphy'
urlpatterns = [
    path("",views.ActorView.as_view(),name='hgraphy'),
    path("api/search-person/", views.person_suggestion, name="person_suggestion"),

]