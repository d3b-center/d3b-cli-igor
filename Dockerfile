FROM python:3.9.18-slim-bullseye

COPY . /
RUN mkdir /root/.aws/
RUN touch /root/.aws/credentials
RUN ./setup.sh
