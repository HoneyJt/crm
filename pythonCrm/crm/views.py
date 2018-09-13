from django.shortcuts import render

from crm import models

# Create your views here.


def index(request):
    # roles = models.UserProfile.objects.all()
    return render(request,'index.html')


