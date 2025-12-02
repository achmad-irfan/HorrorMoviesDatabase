from django.shortcuts import render
import requests
from django.shortcuts import render
from django.views.generic import ListView


# Daftar bahasa tetap dikirim ke template
def index(request):
    return render(request,'search/index.html')
    