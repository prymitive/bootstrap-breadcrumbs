bootstrap-breadcrumbs
=====================

Django template tags used to generate breadcrumbs html using twitter bootstrap css classes.

Requirements:

  * django (tested with 1.4.1)
  * Twitter Bootstrap 2 (tested with 2.1)

Installation
============

Just install it using pip:

    pip install django-bootstrap-breadcrumbs

After that make necessary changes to Django settings:

  * add "django_bootstrap_breadcrumbs" to INSTALLED_APPS.
  * make sure that TEMPLATE_CONTEXT_PROCESSORS contains "django.core.context_processors.request".

Usage
=====

Use {% breadcrumb %} template tag to append all breadcrumbs links, syntax:

    {% breadcrumb $label $viewname [*args] %}

    label - Breadcrumb link text.
    viewname - Any string that can be resolved into view url with django reverse() function or django Model instance with implemented get_absolute_url() method.
    args - Optional arguments to django's reverse() function.

viewname will be resolved into url using django reverse() function using:

    url = resolve(viewname, args=args)

If viewname cannot be resolved using reverse() than it will be rendered as is, so that static
url's can be used in {% breadcrumb %} template tags.

Note that label is escaped by default, so all HTML tags will be replaced. If this is not the desired behaviour use breadcrumb_safe version, it works just like breadcrumb but it doesn't do any escaping.

Finally use {% render_breadcrumbs %} to render all breadcrumbs links to html.
Remeber to use tags inside {% block %}.

Example
=======

base.html:

    {% load django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {% breadcrumb "Home" "/" %}
        {% breadcrumb "Users and groups" "users_and_groups_index" %}
    {% endblock %}

    {% block content %}
        {% render_breadcrumbs %}
    {% endblock %}

users.html:

    {% extends "base.html" %}

    {% load django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {{ block.super }}
        {% breadcrumb "Users" "users.views.index" %}
    {% endblock %}

profile.html:

    {% extends "users.html" %}

    {% load django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {{ block.super }}
        {% breadcrumb user "users.views.profile" user.username %}
    {% endblock %}

Result:

    Home / Users and groups / Users / John Doe

It's also possible to use properties.

profile.html:

    {% extends "users.html" %}

    {% load django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {{ block.super }}
        {% breadcrumb user.email "users.views.profile" user.username %}
    {% endblock %}

Result:

    Home / Users and groups / Users / john.doe@example.org

Changelog
=========

* 0.3.2 - added breadcrumb_safe tag