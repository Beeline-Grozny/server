FROM python:3.10.12-alpine

WORKDIR /app

ADD ./main.py ./

USER 1001