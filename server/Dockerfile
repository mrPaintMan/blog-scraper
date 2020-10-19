FROM python:3.8.0-alpine

WORKDIR /server
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY /server_src /server/server_src
COPY /gunicorn_config.py ./

EXPOSE 5000

CMD gunicorn -c gunicorn_config.py server_src.main:app