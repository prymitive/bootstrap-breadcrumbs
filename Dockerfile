FROM debian:jessie

RUN apt-get update && apt-get install -y python3-dev python3-pip libyaml-dev && apt-get clean

RUN mkdir /src

COPY requirements*.txt MANIFEST.in setup.py .coveragerc conftest.py /src/

RUN pip3 install six
RUN pip3 install -r /src/requirements-test.txt

COPY tests /src/tests

COPY django_bootstrap_breadcrumbs /src/django_bootstrap_breadcrumbs

ARG DJANGO=
RUN pip3 install django${DJANGO}

RUN cd /src && python3 setup.py develop

RUN pip3 freeze | grep -i django
RUN cd /src && coverage run --rcfile=.coveragerc `which py.test` -v -s --pep8 && coverage report -m
