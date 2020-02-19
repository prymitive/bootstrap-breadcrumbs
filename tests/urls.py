# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals


from django import VERSION

if VERSION >= (2, 1):
    from django.contrib.auth.views import LoginView
    login = LoginView.as_view()
else:
    from django.contrib.auth.views import login

if VERSION < (1, 8):  # pragma: nocover
    from django.conf.urls import url, include, patterns
    nsurlpatters = patterns(
        '',
        url(r'^login2$', 'django.contrib.auth.views.login', name='login2_url'),
    )

    urlpatterns = patterns(
        '',
        url(r'^login$', 'django.contrib.auth.views.login', name='login_url'),
        url(r'^login/(?P<slug>[-_\w]+)$', 'django.contrib.auth.views.login',
            name='login_args_url'),
        url(r'^login/user/(?P<user_id>\S+)$',
            'django.contrib.auth.views.login',
            name='login_kwargs_url'),
        (r'^ns/', include(nsurlpatters, namespace='ns')),
    )
elif VERSION < (2, 0):
    from django.conf.urls import url, include
    nsurlpatters = [
        url(r'^login2$', login, name='login2_url'),
    ]

    urlpatterns = [
        url(r'^login$', login, name='login_url'),
        url(r'^login/(?P<slug>[-_\w]+)$', login, name='login_args_url'),
        url(r'^login/user/(?P<user_id>\S+)$', login, name='login_kwargs_url'),
        url(r'^ns/', include(nsurlpatters, namespace='ns')),
    ]
else:
    from django.urls import include, path, re_path
    nsurlpatters = [
        path('login2', login, name='login2_url'),
    ]

    urlpatterns = [
        path('login', login, name='login_url'),
        re_path(r'^login/(?P<slug>[-_\w]+)$', login, name='login_args_url'),
        re_path(r'^login/user/(?P<user_id>\S+)$', login,
                name='login_kwargs_url'),
        path('ns/', include((nsurlpatters, 'ns'), namespace='ns')),
    ]
