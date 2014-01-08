# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from django.conf import settings


def pytest_configure():
    settings.configure(
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'}},
        CACHES={'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}},
        INSTALLED_APPS=('django_bootstrap_breadcrumbs',),
        ROOT_URLCONF='tests.urls'
    )
