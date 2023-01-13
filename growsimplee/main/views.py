from django.shortcuts import render
from django.http import JsonResponse
from .algorithm import *

# Create your views here.





def home(request):
    a = master()
    return JsonResponse({"a" : a})