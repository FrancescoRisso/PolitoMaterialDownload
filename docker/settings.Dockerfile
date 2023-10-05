FROM python:3.7

WORKDIR /copy-settings

RUN apt update && apt -y install nano

COPY ./waitUpdatingSettings.py ./updateSettings.py
COPY ./healthChecker.py ./healthChecker.py

CMD python3 ./updateSettings.py
