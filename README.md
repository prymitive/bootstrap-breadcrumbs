bootstrap-breadcrumbs
=====================

Django template tags used to generate breadcrumbs html using twitter bootstrap css classes.

Requirements:

  * django (tested with 1.4.1)
  * Twitter Bootstrap 2 (tested with 2.1)

Usage
=====

Add "django_bootstrap_breadcrumbs" to INSTALLED_APPS.

Use {% breadcrumb %} template tag to append all breadcrumbs links, syntax:

    {% breadcrum $label $viewname [*args] %}

    label - Breadcrumb link text.
    viewname - Any string that can be resolved into view url with django reverse() function.
    args - Optional arguments to django's reverse() function.

viename will be resolved into url using django reverse() function using:

    url = resolve(viename, args=args)

If viename cannot be resolved using reverse() than it will be rendered as is, so that static
url's can be used in {% breadcrumb %} template tags.

Finally use {% render_breadcrumbs %} to render all breadcrumbs links to html.
Remeber to use tags inside {% block %}.

Example
=======

base.html:

    {% django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {% breadcrumb "Home" "/" %}
        {% breadcrumb "Users and groups" "users_and_groups_index" %}
    {% endblock %}

    {% block content %}
        {% render_breadcrumbs %}
    {% endblock %}

users.html:

    {% extends "base.html" %}

    {% django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {{ block.super }}
        {% breadcrumb "Users" "users.views.index" %}
    {% endblock %}

profile.html:

    {% extends "users.html" %}

    {% django_bootstrap_breadcrumbs %}

    {% block breadcrumbs %}
        {{ block.super }}
        {% breadcrumb user.get_full_name "users.views.profile" user.username %}
    {% endblock %}
