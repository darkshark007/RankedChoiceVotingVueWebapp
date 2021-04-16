# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from rcvserver.models import TYPE_CHOICES
# Create your views here.


@ensure_csrf_cookie
def index(request):
    context = {
        # For setting App-Wide Global Constants, defined in Python, injected to JS
        'javascript_variables': {
            'API': {
                'create_or_update_poll': '/api/create_or_update_poll/',
                'get_poll_data': '/api/get_poll_data/',
                'get_my_polls': '/api/get_my_polls/',
            },
            'POLL_TYPES': TYPE_CHOICES,
        }
    }
    for key in context['javascript_variables']:
        context['javascript_variables'][key] = json.dumps(context['javascript_variables'][key])
    return render(request, 'main.html', context)

