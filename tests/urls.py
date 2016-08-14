# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from django.conf.urls import url, include
import django.contrib.auth.views


nsurlpatters = [
    url(r'^login2$', django.contrib.auth.views.login, name='login2_url'),
]


urlpatterns = [
    url(r'^login$', django.contrib.auth.views.login, name='login_url'),
    url(r'^login/(?P<slug>[-_\w]+)$', django.contrib.auth.views.login,
        name='login_args_url'),
    url(r'^login/user/(?P<user_id>\S+)$', django.contrib.auth.views.login,
        name='login_kwargs_url'),
    (r'^ns/', include(nsurlpatters, namespace='ns')),
]
