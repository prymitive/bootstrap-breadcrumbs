FROM debian:jessie

LABEL maintainer "Łukasz Mierzwa <l.mierzwa@gmail.com>"

RUN apt-get update && apt-get install --no-install-recommends -y python3-dev python3-pip libyaml-dev git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /src

COPY requirements*.txt MANIFEST.in setup.py conftest.py /src/

RUN pip3 install -U pip
RUN pip3 install -U six
RUN pip3 install -U -r /src/requirements-test.txt

COPY tests /src/tests

COPY django_bootstrap_breadcrumbs /src/django_bootstrap_breadcrumbs

ARG DJANGO=
RUN pip3 install "django${DJANGO}"

RUN (cd /src && python3 setup.py develop)

RUN pip3 freeze | grep -i django
RUN (cd /src && py.test -v --pep8 --cov=django_bootstrap_breadcrumbs)
