from django.contrib import admin
from django.urls import path,include
from . import views


app_name='app_movies'
urlpatterns = [
    path("",views.index,name='movies'),
    path("movie/<int:movie_id>/", views.detail_movie, name="detail_movie"),
    path('search-api/', views.search_api, name='search_api')

]

