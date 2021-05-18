from django.urls import path
from . import views

urlpatterns = [
    path('', views.input),
    path('search', views.search),
    path('output', views.output),
    path('loading', views.loading),
]