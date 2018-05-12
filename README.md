django-bootstrap-breadcrumbs
============================

[![Version](https://img.shields.io/pypi/v/django-bootstrap-breadcrumbs.svg)](https://pypi.python.org/pypi/django-bootstrap-breadcrumbs)

See https://django-bootstrap-breadcrumbs.readthedocs.org/en/latest/


Testing
=======

Included Dockerfile allows to run tests using python3 from debian jessie.

Test with the most recent django version::

    docker build .

To specify django version to use for testing set the version via DJANGO arg to docker::

    docker build --build-arg DJANGO===1.9.1 .

DJANGO argument will be passed to pip using `pip install Django${DJANGO}`, so you can pass any version string pip accepts (==version, >=version).

To make testing easier there is a Makefile provided which wraps docker commands.

Run tests agains multiple versions of Django set in Makefile::

    make

To run tests against any version run::

    make $VERSION

Example::

    make 1.10.2
