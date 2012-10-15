#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2012 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from setuptools import setup, find_packages


setup(
    name='django_bootstrap_breadcrumbs',
    version='0.1',
    license='GPLv3',
    description='Django breadcrumbs using Twitter Bootstrap V2',
    long_description='Django template tags used to generate breadcrumbs html using twitter bootstrap css classes',
    author='Łukasz Mierzwa',
    author_email='l.mierzwa@gmail.com',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=['any'],
)
