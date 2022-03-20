from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime

# Create your views here.
def index(request):
    now = datetime.now()
    context = {
        'current_date':now
    }
    return render(request, 'index.html', context)


def select(request):
    context={'num':4}
    return render(request, 'select.html', context)


def result(request):
    context = {}
    return render(request, 'result.html', context)