FROM ubuntu:20.04

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 

WORKDIR /code

# Update e Upgrade dos apps
RUN apt -y update
RUN apt -y upgrade


# Instalando Dependencia dos aplicativos e Chrome webdriver
RUN apt -y install libpq-dev python3-dev

RUN apt install -yqq unzip curl wget python3-pip
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3" "start.py" ]