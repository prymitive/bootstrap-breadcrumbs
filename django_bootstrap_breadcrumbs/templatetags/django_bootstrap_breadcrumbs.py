# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from inspect import ismethod

from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.db.models import Model
from django import template


register = template.Library()


CONTEXT_KEY = 'DJANGO_BREADCRUMB_LINKS'


def breadcrumb(context, label, viewname, *args):
    """
    Add link to list of breadcrumbs, usage:

    {% load bubbles_breadcrumbs %}
    {% breadcrumb "Home" "index" %}

    Remember to use it inside {% block %} with {{ block.super }} to get all
    parent breadcrumbs.

    :param label: Breadcrumb link label.
    :param viewname: Name of the view to link this breadcrumb to, or Model
                     instance with implemented get_absolute_url().
    :param args: Any arguments to view function.
    """
    context['request'].META[CONTEXT_KEY] = context['request'].META.get(
        CONTEXT_KEY, []) + [(escape(label), viewname, args)]
    return ''


def breadcrumb_safe(context, label, viewname, *args):
    """
    Same as breadcrumb but label is not escaped.
    """
    context['request'].META[CONTEXT_KEY] = context['request'].META.get(
        CONTEXT_KEY, []) + [(label, viewname, args)]
    return ''


def render_breadcrumbs(context):
    """
    Render breadcrumbs html using twitter bootstrap css classes.
    """
    links = []
    for (label, viewname, args) in context['request'].META.get(
            CONTEXT_KEY, []):
        if isinstance(viewname, Model) and hasattr(
                viewname, 'get_absolute_url') and ismethod(
                viewname.get_absolute_url):
            url = viewname.get_absolute_url()
        else:
            try:
                url = reverse(viewname=viewname, args=args)
            except NoReverseMatch:
                url = viewname
        links.append((url, _(unicode(label)) if label else label))

    if not links:
        return ''

    ret = '<ul class="breadcrumb">'
    total = len(links)
    for (i, (url, label)) in enumerate(links, 1):
        ret += '<li>'
        if total > 1 and i < total:
            ret += '<a href="%s">%s</a>' % (url, label)
            ret += ' <span class="divider">/</span>'
        else:
            ret += label
        ret += '</li>'
    ret += '</ul>'
    return mark_safe(ret)


register.simple_tag(takes_context=True)(breadcrumb)
register.simple_tag(takes_context=True)(breadcrumb_safe)
register.simple_tag(takes_context=True)(render_breadcrumbs)
