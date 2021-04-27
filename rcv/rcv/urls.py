"""rcv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rcvserver.views import index
from rcvserver.api import (
    create_or_update_poll, 
    get_poll_data,
    get_ballot_data,
    get_my_polls,
    create_or_update_ballot,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/create_or_update_poll/', create_or_update_poll),
    url(r'^api/create_or_update_ballot/', create_or_update_ballot),
    url(r'^api/get_poll_data/', get_poll_data),
    url(r'^api/get_ballot_data/', get_ballot_data),
    url(r'^api/get_my_polls/', get_my_polls),
    url(r'^$', index, name='index'),
]
