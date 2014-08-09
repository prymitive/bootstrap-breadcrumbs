#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from setuptools import setup, find_packages


setup(
    name='django_bootstrap_breadcrumbs',
    version='0.7.0',
    url='http://prymitive.github.com/bootstrap-breadcrumbs',
    license='MIT',
    description='Django breadcrumbs using Bootstrap V2 or V3',
    long_description='Django template tags used to generate breadcrumbs html '
                     'using bootstrap css classes or custom template',
    author='Łukasz Mierzwa',
    author_email='l.mierzwa@gmail.com',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=['any'],
    zip_safe=False,
    include_package_data=True,
)
