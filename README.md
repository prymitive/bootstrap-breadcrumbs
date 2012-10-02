bootstrap-breadcrumbs
=====================

Django template tags used to generate breadcrumbs html using twitter bootstrap css classes.

Requirements:

  * Twitter Bootstrap 2 (written with 2.1)

Example
=======

Add "django_bootstrap_breadcrumbs" to INSTALLED_APPS.

base.html:

  {% django_bootstrap_breadcrumbs %}

  {% block breadcrumbs %}
      {% breadcrumb "Home" "site_index" %}
  {% endblock %}

  {% block content %}
      {% render_breadcrumbs %}
  {% endblock %}

users.html:

  {% django_bootstrap_breadcrumbs %}

  {% block breadcrumbs %}
      {{ block.super }}
      {% breadcrumb "Users" "users.views.index" %}
  {% endblock %}

profile.html
  {% django_bootstrap_breadcrumbs %}

  {% block breadcrumbs %}
      {{ block.super }}
      {% breadcrumb "User profile" "users.views.profile" user.username %}
  {% endblock %}
