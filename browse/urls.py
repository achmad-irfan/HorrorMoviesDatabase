from django.urls import path
from . import views

app_name = 'app_browse'

urlpatterns = [
    path("", views.PageMovies.as_view(), name='browse')
]
