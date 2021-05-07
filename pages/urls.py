from django.urls import path
from . import views

urlpatterns = [
    path('', views.input),
    path('output', views.output)
]