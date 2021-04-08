# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'data': {
            'API': {
                'create_or_update_poll': '/api/create_or_update_poll'
            }
        }
    }
    return render(request, 'main.html', context)



def create_or_update_poll(request):
    print('>>> create_or_update_poll invoked')
    print(request)
    print(request.GET)
    data = {}
    response = JsonResponse(data)
    return response