from django.shortcuts import render

# Create your views here.
def index(request):
    context={
        'title':'Kisah'
    }
    return render(request,'kisah/index.html',context)