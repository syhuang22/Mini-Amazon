FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install django-bootstrap-v5
RUN pip install -r requirements.txt

ADD . /code/
