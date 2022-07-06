FROM python:3

ADD . /sendler

RUN pip install aiogram
RUN pip install db-sqlite3

WORKDIR /sendler

CMD [ "python3", "./main.py" ]