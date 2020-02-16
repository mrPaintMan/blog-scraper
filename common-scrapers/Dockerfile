FROM python:3.8

WORKDIR /app
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY /selenium_src /app/src

#ENV PYTHONPATH /app

CMD python3 -m src.main