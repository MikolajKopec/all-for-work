# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
CMD [ "flask", "run", "--host=0.0.0.0", "--debug"]