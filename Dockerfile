# server
FROM ubuntu:17.10

RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install python3-pip -y

WORKDIR /server
COPY ./requirements.txt /server/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /server

# CMD [ 'python3', 'main.py' ]
ENTRYPOINT [ '/bin/bash' ]