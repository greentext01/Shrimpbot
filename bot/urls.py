from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("authorize", views.authorize),
    path("shb", views.shb),
]
