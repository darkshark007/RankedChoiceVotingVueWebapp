# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'days': [1, 2, 3],
    }
    return render(request, 'main.html', context)



def create_or_update_poll(request):
    print('>>> create_or_update_poll invoked')
    print(request)
    return