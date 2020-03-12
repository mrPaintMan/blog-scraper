FROM python:3.8

WORKDIR /app
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY /selenium_src /app/selenium_src

CMD python3 -m selenium_src.main