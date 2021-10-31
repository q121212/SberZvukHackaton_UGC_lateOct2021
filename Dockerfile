# syntax=docker/dockerfile:1
FROM python:3.9.5
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
