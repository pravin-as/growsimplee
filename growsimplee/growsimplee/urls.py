from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]
