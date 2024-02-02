FROM python:3.12.1-alpine

COPY requirements.txt /temp/requirements.txt

COPY  test_project /test_project

WORKDIR /test_project

EXPOSE 8000

RUN pip install -r /temp/requirements.txt
