from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def index(req):
    return render(req, 'index.html')


def result(req):
    return render(req, 'result.html')
