FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /backend

WORKDIR /backend
RUN pip install -Ur requirements.txt