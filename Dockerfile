FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get install -y python3 python3-pip sudo

RUN apt-get install -y caffe-cpu

RUN useradd -m arpit

RUN chown -R arpit:arpit /home/arpit/

COPY --chown=arpit . /home/arpit/app/

USER arpit

RUN cd /home/arpit/app/ && pip3 install -r requirements.txt --no-cache-dir

WORKDIR /home/arpit/app

EXPOSE 8080

ENTRYPOINT python3 main.py
