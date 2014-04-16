# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

import logging
from inspect import ismethod

from django.core.urlresolvers import (reverse, resolve, NoReverseMatch,
                                      Resolver404)
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from django.db.models import Model
from django import template


logger = logging.getLogger(__name__)

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
    if 'request' in context:
        context['request'].META[CONTEXT_KEY] = context['request'].META.get(
            CONTEXT_KEY, []) + [(escape(label), viewname, args)]
    else:
        logger.error("request object not found in context! Check if "
                     "'django.core.context_processors.request' is in "
                     "TEMPLATE_CONTEXT_PROCESSORS")
    return ''


def breadcrumb_safe(context, label, viewname, *args):
    """
    Same as breadcrumb but label is not escaped.
    """
    if 'request' in context:
        context['request'].META[CONTEXT_KEY] = context['request'].META.get(
            CONTEXT_KEY, []) + [(label, viewname, args)]
    else:
        logger.error("request object not found in context! Check if "
                     "'django.core.context_processors.request' is in "
                     "TEMPLATE_CONTEXT_PROCESSORS")
    return ''


def render_breadcrumbs(context, *args):
    """
    Render breadcrumbs html using bootstrap css classes.
    """
    if 'request' not in context:
        logger.error("request object not found in context! Check if "
                     "'django.core.context_processors.request' is in "
                     "TEMPLATE_CONTEXT_PROCESSORS")
        return ''

    if args:
        template_path = args[0]
    else:
        template_path = 'django_bootstrap_breadcrumbs/bootstrap2.html'

    links = []
    for (label, viewname, view_args) in context['request'].META.get(
            CONTEXT_KEY, []):
        if isinstance(viewname, Model) and hasattr(
                viewname, 'get_absolute_url') and ismethod(
                viewname.get_absolute_url):
            url = viewname.get_absolute_url()
        else:
            try:
                try:
                    # 'resolver_match' introduced in Django 1.5
                    current_app = context['request'].resolver_match.namespace
                except AttributeError:
                    try:
                        resolver_match = resolve(context['request'].path)
                        current_app = resolver_match.namespace
                    except Resolver404:
                        current_app = None
                url = reverse(viewname=viewname, args=view_args,
                              current_app=current_app)
            except NoReverseMatch:
                url = viewname
        links.append((url, _(smart_text(label)) if label else label))

    if not links:
        return ''

    return mark_safe(template.loader.render_to_string(
        template_path, {'breadcrumbs': links,
                        'breadcrumbs_total': len(links)}))


class BreadcrumbNode(template.Node):

    def __init__(self, nodelist, viewname, args):
        self.nodelist = nodelist
        self.viewname = viewname
        self.args = args

    def render(self, context):
        if 'request' not in context:
            logger.error("request object not found in context! Check if "
                         "'django.core.context_processors.request' is in "
                         "TEMPLATE_CONTEXT_PROCESSORS")
            return ''
        label = self.nodelist.render(context)
        try:
            viewname = template.Variable(self.viewname).resolve(context)
        except template.VariableDoesNotExist:
            viewname = self.viewname
        args = self.parse_args(context)
        context['request'].META[CONTEXT_KEY] = context['request'].META.get(
            CONTEXT_KEY, []) + [(label, viewname, args)]
        return ''

    def parse_args(self, context):
        args = []
        for arg in self.args:
            try:
                value = template.Variable(arg).resolve(context)
            except template.VariableDoesNotExist:
                value = arg
            args.append(value)
        return args


def breadcrumb_for(parser, token):
    bits = list(token.split_contents())
    end_tag = 'end' + bits[0]
    nodelist = parser.parse((end_tag,))
    parser.delete_first_token()
    return BreadcrumbNode(nodelist, bits[1], bits[2:])


def clear_breadcrumbs(context, *args):
    """
    Removes all currently added breadcrumbs.
    """
    if 'request' not in context:
        logger.error("request object not found in context! Check if "
                     "'django.core.context_processors.request' is in "
                     "TEMPLATE_CONTEXT_PROCESSORS")
        return ''

    if CONTEXT_KEY in context['request'].META:
        del context['request'].META[CONTEXT_KEY]

    return ''


register.simple_tag(takes_context=True)(breadcrumb)
register.simple_tag(takes_context=True)(breadcrumb_safe)
register.simple_tag(takes_context=True)(render_breadcrumbs)
register.simple_tag(takes_context=True)(clear_breadcrumbs)
register.tag('breadcrumb_for', breadcrumb_for)
