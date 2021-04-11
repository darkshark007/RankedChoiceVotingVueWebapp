# -*- coding: utf-8 -*-
import json

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from rcvserver.models import Poll
# Create your views here.


@ensure_csrf_cookie
def index(request):
    context = {
        # For setting App-Wide Global Constants, defined in Python, injected to JS
        'javascript_variables': {
            'API': {
                'create_or_update_poll': '/api/create_or_update_poll'
            },
            'POLL_TYPES': Poll.TYPE_CHOICES,
        }
    }
    for key in context['javascript_variables']:
        context['javascript_variables'][key] = json.dumps(context['javascript_variables'][key])
    return render(request, 'main.html', context)

