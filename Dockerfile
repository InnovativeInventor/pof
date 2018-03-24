FROM python:latest

MAINTAINER InnovativeInventor

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y && apt-get install git -y
RUN git clone https://github.com/InnovativeInventor/pof /usr/src/app
RUN pip3 install gunicorn flask gitpython feedparser requests Flask-Caching
RUN rm Dockerfile

EXPOSE 8000
CMD [ "gunicorn", "app:app", "-w", "4", "--bind", ":8000" ]
