# server
FROM ubuntu:17.10

RUN apt-get update
RUN apt-get install mysql-client -y
RUN apt-get install ffmpeg -y
RUN apt-get install python3-pip -y
RUN apt-get install mongodb-clients -y

WORKDIR /server
COPY ./requirements.txt /server/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /server

ENTRYPOINT ["/bin/bash", "start_script.sh"]
# ENTRYPOINT [ "/bin/bash" ]