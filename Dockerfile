FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN apt update -y
RUN apt install python3-pip -y
#RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip install aiogram
RUN pip install db-sqlite3

#WORKDIR /home/as/Desktop/git/python-sendler-bot/

COPY . ./
CMD [ "python3", "./main.py" ]