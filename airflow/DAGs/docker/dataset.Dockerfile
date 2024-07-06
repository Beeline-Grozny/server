FROM python:3.10.12-alpine

WORKDIR /app

ADD ./dataset_builder.py ./

USER 1001