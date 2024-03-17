FROM python:3.12.1-alpine

RUN mkdir "test_project"

COPY requirements.txt /test_project

COPY  test_project /test_project

WORKDIR /test_project

EXPOSE 8000

RUN pip install -r /test_project/requirements.txt
