FROM python:3.8

# Set the correct timezone
ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install chromium
RUN apt-get update
RUN apt-get install chromium --yes

# install chromedriver
RUN apt-get install chromium-driver --yes

# set display port to avoid crash
ENV DISPLAY=:99

WORKDIR /app
COPY /requirements.txt ./
RUN pip install -r requirements.txt
COPY /selenium_src /app/selenium_src

CMD python3 -m selenium_src.main