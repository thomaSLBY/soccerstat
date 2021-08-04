FROM mongo:latest
RUN apt-get update && apt-get install -y python3 python3-pip
ADD . /mongo
WORKDIR /mongo
RUN pip3 install -r requirements.txt
CMD ["python3", "-u", "main.py"]
EXPOSE 27017