from django.contrib import admin
from django.urls import path, include
from .views import home, ProductView


urlpatterns = [
    path('home/', home),
    path('product/', ProductView.as_view()),
]