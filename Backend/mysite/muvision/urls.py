from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("", csrf_exempt(views.index), name="index"),
    # path("classify_single/", csrf_exempt(views.classify_single), name="classify_single"),
    path("classify_image/", csrf_exempt(views.classify_image), name="classify_image")
]