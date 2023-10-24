FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /tgbot

WORKDIR /tgbot
RUN pip install -Ur requirements.txt