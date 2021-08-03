FROM python:3.8-slim
RUN mkdir /scraping
WORKDIR /scraping
ADD requirements.txt /scraping
RUN pip3 install -r requirements.txt
ADD . /scraping
EXPOSE 8080