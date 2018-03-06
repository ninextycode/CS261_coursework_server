# server
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install apt-transport-https -y
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.6.list
RUN apt-get update

RUN apt-get install ffmpeg -y
RUN apt-get install python3-pip -y
RUN apt-get install mongodb-org -y

RUN apt-get install mysql-server -y

WORKDIR /server
COPY ./requirements.txt /server/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /server

# CMD [ 'python3', 'main.py' ]
ENTRYPOINT [ '/bin/bash' ]