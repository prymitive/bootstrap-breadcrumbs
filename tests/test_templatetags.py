# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from django import VERSION
from django.test import TestCase
from django.template import Context, Template
from django.test.client import RequestFactory
from django.db.models import Model, CharField
from django.test.utils import override_settings
from testfixtures import LogCapture

try:
    from django import setup
except ImportError:
    pass
else:
    setup()


T_LOAD = '{% load django_bootstrap_breadcrumbs %}'

T_BLOCK_CLEAR = '''
{% block breadcrumbs %}
{% clear_breadcrumbs %}
{% endblock %}
'''

T_BLOCK_USER_SAFE_CLEAR = '''
{% block breadcrumbs %}
{% breadcrumb "Home" "/" %}
{% breadcrumb "Login" "login_url" %}
{% breadcrumb actor actor %}
{% breadcrumb "Users and groups" "/users" %}
{% breadcrumb_safe "<span>John</span>" "/john" %}
{% clear_breadcrumbs %}
{% breadcrumb "Cleared" actor %}
{% endblock %}
'''

T_BLOCK_USER = '''
{% block breadcrumbs %}
{% breadcrumb "Home" "/" %}
{% breadcrumb "Users and groups" "/users" %}
{% endblock %}
'''

T_BLOCK_SAFE = '''
{% block breadcrumbs %}
{% breadcrumb_safe "<&>" "/" %}
{% breadcrumb_safe "<span><></span>" "/john" %}
{% endblock %}
'''

T_BLOCK_RAW = '''
{% block breadcrumbs %}
{% breadcrumb_raw "<span>John</span>" "/john" %}
{% endblock %}
'''

T_BLOCK_RAW_SAFE = '''
{% block breadcrumbs %}
{% breadcrumb_raw_safe "<span>John</span>" "/john" %}
{% endblock %}
'''

T_BLOCK_USER_SAFE = '''
{% block breadcrumbs %}
{% breadcrumb "<" "/" %}
{% breadcrumb "Login" "login_url" %}
{% breadcrumb actor actor %}
{% breadcrumb "Users and groups" "/users" %}
{% breadcrumb_safe "<span>John</span>" "/john" %}
{% endblock %}
'''

T_BLOCK_NS = '''
{% block breadcrumbs %}
{% breadcrumb "Login2" "ns:login2_url" %}
{% breadcrumb "John" "/john" %}
{% endblock %}
'''

T_BLOCK_NS_FOR = '''
{% block breadcrumbs %}
{% breadcrumb_for "/static" %}<span>Static</span>{% endbreadcrumb_for %}
{% breadcrumb_for ns:login2_url %}Login2{% endbreadcrumb_for %}
{% breadcrumb_for "/john" %}John{% endbreadcrumb_for %}
{% endblock %}
'''

T_BLOCK_NS_FOR_QUOTES = '''
{% block breadcrumbs %}
{% breadcrumb_for "ns:login2_url" %}Login2a{% endbreadcrumb_for %}
{% breadcrumb_for 'ns:login2_url' %}Login2b{% endbreadcrumb_for %}
{% breadcrumb_for "/john" %}John{% endbreadcrumb_for %}
{% endblock %}
'''

T_BLOCK_ESCAPE = '''
{% block breadcrumbs %}
{% breadcrumb "Home" "/" %}
{% breadcrumb "<span>John</span>" "/john" %}
{% endblock %}
'''

T_BLOCK_FOR = '''
{% block breadcrumbs %}
{% breadcrumb_for "/static" %}<span>Static</span>{% endbreadcrumb_for %}
{% breadcrumb_for actor %}{{ actor.name }}{% endbreadcrumb_for %}
{% endblock %}
'''

T_BLOCK_FOR_VAR = '''
{% block breadcrumbs %}
{% breadcrumb_for nonexisting %}404{% endbreadcrumb_for %}
{% breadcrumb_for login_args_url actor.name %}Login Act{% endbreadcrumb_for %}
{% breadcrumb_for login_args_url dummyarg %}Login Actor{% endbreadcrumb_for %}
{% breadcrumb "Home" "/" %}
{% endblock %}
'''

T_BLOCK_KWARGS = '''
{% block breadcrumbs %}
{% breadcrumb "User 12345" "login_kwargs_url" user_id=12345 %}
{% breadcrumb "Home" "/" %}
{% endblock %}
'''

T_BLOCK_FOR_KWARGS = '''
{% block breadcrumbs %}
{% breadcrumb_for login_kwargs_url user_id=dummyarg %}KV{% endbreadcrumb_for %}
{% breadcrumb_for login_kwargs_url user_id=actor.name %}{% endbreadcrumb_for %}
{% breadcrumb "Home" "/" %}
{% endblock %}
'''

T_BLOCK_KWARGS_MODEL = '''
{% block breadcrumbs %}
{% breadcrumb actor actor %}
{% breadcrumb actor actor id=12345 %}
{% breadcrumb "Home" "/" %}
{% endblock %}
'''

T_BLOCK_FOR_KWARGS_MODEL = '''
{% block breadcrumbs %}
{% breadcrumb_for actor %}actor{% endbreadcrumb_for %}
{% breadcrumb_for actor id=actor.name %}actor{% endbreadcrumb_for %}
{% breadcrumb_for actor id=12345 order=abc %}actor{% endbreadcrumb_for %}
{% breadcrumb "Home" "/" %}
{% endblock %}
'''

T_BLOCK_EMPTY_URL = '''
{% block breadcrumbs %}
{% breadcrumb_for "" %}Home For{% endbreadcrumb_for %}
{% breadcrumb "Home" "" %}
{% endblock %}
'''

T_BLOCK_RENDER_BS2 = '''
{% block content %}
<div>{% render_breadcrumbs %}</div>
{% endblock %}
'''

T_BLOCK_RENDER_BS3 = '''
{% block content %}
<div>
{% render_breadcrumbs "django_bootstrap_breadcrumbs/bootstrap3.html" %}
</div>
{% endblock %}
'''

T_BLOCK_RENDER_BS4 = '''
{% block content %}
<div>
{% render_breadcrumbs "django_bootstrap_breadcrumbs/bootstrap4.html" %}
</div>
{% endblock %}
'''


class Actor(Model):

    name = CharField(max_length=128)

    def get_absolute_url(self, *args, **kwargs):
        if kwargs and 'id' in kwargs and 'order' in kwargs:
            return '/actor/%s/details/%s' % (kwargs['id'], kwargs['order'])
        elif kwargs and 'id' in kwargs:
            return '/actor/%s' % kwargs['id']
        return '/actor'

    class Meta:
        app_label = 'test_app'


@override_settings(
    INSTALLED_APPS=['django', 'django.contrib.auth',
                    'django_bootstrap_breadcrumbs', 'tests'],
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True}]
    )
class SiteTests(TestCase):

    def setUp(self):
        self.actor = Actor(name='Actor')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.context = Context({'request': self.request, 'actor': self.actor})

    def assertRequestError(self, log):
        message = str(log)
        self.assertIn('ERROR', message)
        self.assertIn('not found', message)
        if VERSION < (1, 8):
            self.assertIn('django.core.context_processors.request', message)
            self.assertIn('TEMPLATE_CONTEXT_PROCESSORS', message)
        else:
            self.assertIn('django.template.context_processors.request',
                          message)
            self.assertIn('context_processors', message)

    def test_load(self):
        t = Template(T_LOAD)
        self.assertEqual(t.render(self.context), '')

    def test_clear_breadcrumbs(self):
        t = Template(T_LOAD + T_BLOCK_CLEAR)
        self.assertEqual(t.render(self.context), '\n\n\n\n')

    def test_clear_breadcrumbs_without_request(self):
        t = Template(T_LOAD + T_BLOCK_CLEAR)
        with LogCapture() as log:
            self.assertEqual(t.render(Context()), '\n\n\n\n')
        self.assertRequestError(log)

    def test_push_breadcrumbs(self):
        t = Template(T_LOAD + T_BLOCK_USER)
        self.assertEqual(t.render(self.context), '\n\n\n\n\n')

    def test_push_breadcrumb_for(self):
        t = Template(T_LOAD + T_BLOCK_FOR)
        self.assertEqual(t.render(self.context), '\n\n\n\n\n')

    def test_push_breadcrumb_for_without_request(self):
        t = Template(T_LOAD + T_BLOCK_FOR)
        with LogCapture() as log:
            self.assertEqual(t.render(Context()), '\n\n\n\n\n')
        self.assertRequestError(log)

    def test_push_breadcrumbs_safe(self):
        t = Template(T_LOAD + T_BLOCK_SAFE)
        self.assertEqual(t.render(self.context), '\n\n\n\n\n')

    def test_push_breadcrumbs_raw(self):
        t = Template(T_LOAD + T_BLOCK_RAW)
        self.assertEqual(t.render(self.context), '\n\n\n\n')

    def test_push_breadcrumbs_raw_safe(self):
        t = Template(T_LOAD + T_BLOCK_RAW_SAFE)
        self.assertEqual(t.render(self.context), '\n\n\n\n')

    def test_render_empty_url_bs2(self):
        t = Template(T_LOAD + T_BLOCK_EMPTY_URL + T_BLOCK_RENDER_BS2)
        self.assertHTMLEqual(t.render(self.context),
                             '<div><ul class="breadcrumb">'
                             '<li>Home For<span class="divider">/</span></li>'
                             '<li>Home</li>'
                             '</ul></div>')

    def test_render_empty_url_bs3(self):
        t = Template(T_LOAD + T_BLOCK_EMPTY_URL + T_BLOCK_RENDER_BS3)
        self.assertHTMLEqual(t.render(self.context),
                             '<div><ul class="breadcrumb">'
                             '<li>Home For</li>'
                             '<li class="active">Home</li>'
                             '</ul></div>')

    def test_render_empty_url_bs4(self):
        t = Template(T_LOAD + T_BLOCK_EMPTY_URL + T_BLOCK_RENDER_BS4)
        self.assertHTMLEqual(t.render(self.context),
                             '<div><nav class="breadcrumb">'
                             '<span class="breadcrumb-item">Home For</span>'
                             '<span class="breadcrumb-item active">Home</span>'
                             '</nav></div>')

    def test_render_empty_breadcrumbs_bs2(self):
        t = Template(T_LOAD + T_BLOCK_RENDER_BS2)
        self.assertEqual(t.render(self.context), '\n\n<div></div>\n\n')

    def test_render_empty_breadcrumbs_bs3(self):
        t = Template(T_LOAD + T_BLOCK_RENDER_BS3)
        self.assertEqual(t.render(self.context), '\n\n<div>\n\n</div>\n\n')

    def test_render_empty_breadcrumbs_bs4(self):
        t = Template(T_LOAD + T_BLOCK_RENDER_BS4)
        self.assertEqual(t.render(self.context), '\n\n<div>\n\n</div>\n\n')

    def test_render_without_request(self):
        t = Template(T_LOAD + T_BLOCK_USER_SAFE + T_BLOCK_RENDER_BS2)
        with LogCapture() as log:
            self.assertNotEqual(t.render(Context()), '')
        self.assertRequestError(log)

    def test_render(self):
        t = Template(T_LOAD + T_BLOCK_USER_SAFE + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/">&lt;</a>' in resp)
        self.assertTrue('<a href="/login">Login</a>' in resp)
        self.assertTrue('<a href="/actor">Actor object</a>' in resp)
        self.assertTrue('<a href="/users">Users and groups</a>' in resp)
        self.assertTrue('<span>John</span>' in resp)
        self.assertTrue('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 5)

    def test_render_safe(self):
        t = Template(T_LOAD + T_BLOCK_SAFE + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/"><&></a>' in resp)
        self.assertTrue('<span><></span>' in resp)
        self.assertTrue('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 2)

    def test_render_bs3(self):
        t = Template(T_LOAD + T_BLOCK_USER_SAFE + T_BLOCK_RENDER_BS3)
        resp = t.render(self.context)
        self.assertTrue('<a href="/">&lt;</a>' in resp)
        self.assertTrue('<a href="/login">Login</a>' in resp)
        self.assertTrue('<a href="/actor">Actor object</a>' in resp)
        self.assertTrue('<a href="/users">Users and groups</a>' in resp)
        self.assertTrue('<span>John</span>' in resp)
        self.assertFalse('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 5)

    def test_render_bs4(self):
        t = Template(T_LOAD + T_BLOCK_USER_SAFE + T_BLOCK_RENDER_BS4)
        resp = t.render(self.context)
        self.assertTrue('<a class="breadcrumb-item" href="/">&lt;</a>' in resp)
        self.assertTrue('<a class="breadcrumb-item" href="/login">'
                        'Login</a>' in resp)
        self.assertTrue('<a class="breadcrumb-item" href="/actor">'
                        'Actor object</a>' in resp)
        self.assertTrue('<a class="breadcrumb-item" href="/users">'
                        'Users and groups</a>' in resp)
        self.assertTrue('<span class="breadcrumb-item active"><span>'
                        'John</span></span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 5)

    @override_settings(
        BREADCRUMBS_TEMPLATE='django_bootstrap_breadcrumbs/bootstrap3.html')
    def test_render_bs3_using_settings(self):
        t = Template(T_LOAD + T_BLOCK_USER_SAFE + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/">&lt;</a>' in resp)
        self.assertTrue('<a href="/login">Login</a>' in resp)
        self.assertTrue('<a href="/actor">Actor object</a>' in resp)
        self.assertTrue('<a href="/users">Users and groups</a>' in resp)
        self.assertTrue('<span>John</span>' in resp)
        self.assertFalse('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 5)

    @override_settings(
        BREADCRUMBS_TEMPLATE='django_bootstrap_breadcrumbs/bootstrap4.html')
    def test_render_bs4_using_settings(self):
        t = Template(T_LOAD + T_BLOCK_USER_SAFE + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a class="breadcrumb-item" href="/">&lt;</a>' in resp)
        self.assertTrue('<a class="breadcrumb-item" href="/login">'
                        'Login</a>' in resp)
        self.assertTrue('<a class="breadcrumb-item" href="/actor">'
                        'Actor object</a>' in resp)
        self.assertTrue('<a class="breadcrumb-item" href="/users">'
                        'Users and groups</a>' in resp)
        self.assertTrue('<span class="breadcrumb-item active"><span>'
                        'John</span></span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 5)

    def test_render_breadcrumb_for(self):
        t = Template(T_LOAD + T_BLOCK_FOR + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/static"><span>Static</span></a>' in resp)
        self.assertTrue('Actor' in resp)
        self.assertTrue('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 2)

    def test_render_breadcrumb_for_variable(self):
        t = Template(T_LOAD + T_BLOCK_FOR_VAR + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="nonexisting">404</a>' in resp)
        self.assertTrue('<a href="/login/Actor">Login Act</a>' in resp)
        self.assertTrue('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 4)

    def test_render_breadcrumb_kwargs(self):
        t = Template(T_LOAD + T_BLOCK_KWARGS + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/login/user/12345">User 12345</a>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 2)

    def test_render_breadcrumb_for_kwargs(self):
        t = Template(T_LOAD + T_BLOCK_FOR_KWARGS + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/login/user/dummyarg">KV</a>' in resp)
        self.assertTrue('<a href="/login/user/Actor"></a>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 3)

    def test_render_breadcrumb_kwargs_model(self):
        t = Template(T_LOAD + T_BLOCK_KWARGS_MODEL + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/actor">Actor object</a>' in resp)
        self.assertTrue('<a href="/actor/12345">Actor object</a>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 3)

    def test_render_breadcrumb_for_kwargs_model(self):
        t = Template(T_LOAD + T_BLOCK_FOR_KWARGS_MODEL + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/actor">actor</a>' in resp)
        self.assertTrue('<a href="/actor/Actor">actor</a>' in resp)
        self.assertTrue(
            '<a href="/actor/12345/details/abc">actor</a>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 4)

    def test_render_ns(self):
        t = Template(T_LOAD + T_BLOCK_NS + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/ns/login2">Login2</a>' in resp)
        self.assertTrue('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 2)

    def test_render_ns_app(self):
        self.context['request'].path = '/login'
        t = Template(T_LOAD + T_BLOCK_NS + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/ns/login2">Login2</a>' in resp)
        self.assertTrue('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 2)

    def test_render_ns_breadcrumb_for(self):
        t = Template(T_LOAD + T_BLOCK_NS_FOR + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/static"><span>Static</span></a>' in resp)
        self.assertTrue('<a href="/ns/login2">Login2</a>' in resp)
        self.assertTrue('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 3)

    def test_render_ns_breadcrumb_for_quotes(self):
        t = Template(T_LOAD + T_BLOCK_NS_FOR_QUOTES + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('<a href="/ns/login2">Login2a</a>' in resp)
        self.assertTrue('<a href="/ns/login2">Login2b</a>' in resp)
        self.assertTrue('<span class="divider">/</span>' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 3)

    def test_render_escape(self):
        t = Template(T_LOAD + T_BLOCK_ESCAPE + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertTrue('&lt;span&gt;John&lt;/span&gt;' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 2)

    def test_render_cleared(self):
        t = Template(T_LOAD + T_BLOCK_USER_SAFE_CLEAR + T_BLOCK_RENDER_BS2)
        resp = t.render(self.context)
        self.assertFalse('<a href="/">Home</a>' in resp)
        self.assertFalse('<a href="/login">Login</a>' in resp)
        self.assertFalse('<a href="/actor">Actor object</a>' in resp)
        self.assertFalse('<a href="/users">Users and groups</a>' in resp)
        self.assertFalse('<span>John</span>' in resp)
        self.assertFalse('<span class="divider">/</span>' in resp)
        self.assertTrue('Cleared' in resp)
        self.assertEqual(len(self.request.META['DJANGO_BREADCRUMB_LINKS']), 1)
