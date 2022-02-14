FROM python:3.8-buster

WORKDIR /household-chores

ADD . /household-chores
WORKDIR /household-chores
RUN apt-get install iputils-ping -y
RUN pip install -r requirements.txt

CMD [ "python", "./start.py" ]