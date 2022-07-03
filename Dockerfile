FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN apt update -y
RUN apt install python3-pip -y
RUN pip install aiogram
RUN pip install db-sqlite3

CMD [ "python3", "./main.py" ]