FROM python:3.8

WORKDIR /app
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY /common_src /app/common_src

CMD python3 -m common_src.main