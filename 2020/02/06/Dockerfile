# Base docker image
FROM python:3.7.4-alpine 
LABEL maintainer "Ethan Gregory Dodge <ethan@egd.io>"

COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt
RUN rm -f /root/requirements.txt

WORKDIR /root

ENTRYPOINT [ "python3" ]
