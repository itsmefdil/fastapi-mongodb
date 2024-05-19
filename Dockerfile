FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt .

RUN apk update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
