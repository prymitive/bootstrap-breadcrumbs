.. django-bootstrap-breadcrumbs documentation master file, created by
   sphinx-quickstart on Sat Jun  8 17:00:11 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-bootstrap-breadcrumbs's documentation!
========================================================

Links
=====

Homepage: https://github.com/prymitive/bootstrap-breadcrumbs

Issue tracker: https://github.com/prymitive/bootstrap-breadcrumbs/issues

Installation
============

Just install it using pip (recommended)::

    pip install django-bootstrap-breadcrumbs

Or clone it from github::

    git clone https://github.com/prymitive/bootstrap-breadcrumbs.git
    cd bootstrap-breadcrumbs
    ./setup.py install

After that make necessary changes to Django settings::

   * add "django_bootstrap_breadcrumbs" to INSTALLED_APPS.
   * make sure that TEMPLATE_CONTEXT_PROCESSORS contains "django.core.context_processors.request".

Declaring breadcrumbs
=====================

There are currently three tags for adding breadcrumbs for pages (remeber to use tags inside ``{% block %}``):

``{% breadcrumb %}``
~~~~~~~~~~~~~~~~~~~~

Syntax::

    {% breadcrumb $label $viewname [*args] %}


``label`` - Breadcrumb link text.

``viewname`` - Any string that can be resolved into view url with django reverse() function or django Model instance with implemented ``get_absolute_url()`` method.

``args`` - Optional arguments to django's ``reverse()`` function.

viewname will be resolved into url using django ``reverse()`` function using::

    url = resolve(viewname, args=args)

If viewname cannot be resolved using reverse() than it will be rendered as is, so that static
url's can be used in ``{% breadcrumb %}`` template tags.

Note that label is escaped by default, so all HTML tags will be replaced.
This is protection for cases where label can contain user provided content, for example username.
If user would somehow put links or javascript into the label, he could expose any viewer to malicious code.

Example::

    {% block breadcrumbs %}
        {% breadcrumb "Home" "/" %}
        {% breadcrumb "Users and groups" "users_and_groups_index" %}
    {% endblock %}

label can be anything that django template will resolve::

    {% block breadcrumbs %}
        {% breadcrumb user.username "user_profile" user.id %}
    {% endblock %}

``{% breadcrumb_safe %}``
~~~~~~~~~~~~~~~~~~~~~~~~~

It works just like ``{% breadcrumb %}`` but it doesn't do any escaping, use it if trusted HTML is required in the label.

Example::

    {% block breadcrumbs %}
        {% breadcrumb_safe "<i class='icon-home'></i>Home" "/" %}
    {% endblock %}

``{% breadcrumb_for %}``
~~~~~~~~~~~~~~~~~~~~~~~~

Starting with 0.4.0 there is also block tag, usage::

    {% breadcrumb_for $viewname [*args] %}
        $label
    {% endbreadcrumb_for %}

Any code can be used there, it won't be escaped in any way.
It gives the possibility to fully control the label content and for example escape only parts of it.

Examples::

    {% breadcrumb_for site_index %}
        <i class='icon-home'></i>
        {% trans "Home" %}
    {% endbreadcrumb_for %}

    {% breadcrumb_for user_profile user.username %}
        <i class='icon-user'></i>
        {{ user.username }}
    {% endbreadcrumb_for %}

Rendering breadcrumbs
=====================

To render breadcrumbs as HTML use ``{% render_breadcrumbs %}``.

Example::

    {% block content %}
        {% render_breadcrumbs %}
    {% endblock %}

Starting with 0.5.0 it's possible to use custom template to integrate breadcrumbs with frameworks other than Twitter Bootstrap.

Example::

    {% block content %}
        {% render_breadcrumbs "path/to/my/template.html %}
    {% endblock %}

Default template uses Twitter Bootstrap classes::

    <ul class="breadcrumb">
        {% for url, label in breadcrumbs %}
            <li>
                {% ifnotequal forloop.counter breadcrumbs_total %}
                    <a href="{{ url }}">{{ label|safe }}</a>
                {% else %}
                    {{ label|safe }}
                {% endifnotequal %}
                {% if not forloop.last %}
                    <span class="divider">/</span>
                {% endif %}
            </li>
        {% endfor %}
    </ul>

* breadcrumbs - list of breadcrumbs elements, each element contains url and label
* breadcrumbs_total - total number of breadcrumbs elements

Full examples
=============

base.html::

    {% load django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {% breadcrumb "Home" "/" %}
        {% breadcrumb "Users and groups" "users_and_groups_index" %}
    {% endblock %}

    {% block content %}
        {% render_breadcrumbs %}
    {% endblock %}

users.html::

    {% extends "base.html" %}

    {% load django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {{ block.super }}
        {% breadcrumb "Users" "users.views.index" %}
    {% endblock %}

profile.html::

    {% extends "users.html" %}

    {% load django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {{ block.super }}
        {% breadcrumb user "users.views.profile" user.username %}
    {% endblock %}

Result::

    Home / Users and groups / Users / John Doe

It's also possible to use properties.

profile.html::

    {% extends "users.html" %}

    {% load django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {{ block.super }}
        {% breadcrumb user.email "users.views.profile" user.username %}
    {% endblock %}

Result::

    Home / Users and groups / Users / john.doe@example.org

Changelog
=========

* 0.5.1 - added missing template to the package
* 0.5.0 - HTML rendering was moved to template with possibility to use custom templates
* 0.4.0 - added breadcrumb_for block tag
* 0.3.3 - fixed typo in 0.3.2
* 0.3.2 - added breadcrumb_safe tag

Contributors
============

Author: Łukasz Mierzwa <l.mierzwa [at] gmail>

Contributors:

* Ewoud Kohl van Wijngaarden
* gnuwho
* Christian Dullweber

Bug reports
===========

Use GitHub: https://github.com/prymitive/bootstrap-breadcrumbs/issues
