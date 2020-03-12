FROM python:3.8

WORKDIR /app
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY /common_src /app/src

CMD python3 -m src.main