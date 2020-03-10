FROM python:3.8

WORKDIR /server
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY /server_src /server/server_src

EXPOSE 5000

CMD python3 -m server_src.main