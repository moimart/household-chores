FROM python:3.8

WORKDIR /household-chores

ADD . /household-chores
WORKDIR /household-chores
RUN pip install -r requirements.txt

CMD [ "python", "./start.py" ]