FROM python:3.8

# Set the correct timezone
ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY /common_src /app/common_src

CMD python3 -m common_src.main