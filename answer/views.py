from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def answer_list(request):
    return HttpResponse("ok")
