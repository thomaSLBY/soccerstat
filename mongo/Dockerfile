FROM mongo:latest
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install pymongo
WORKDIR /app
COPY . .
CMD ["python3", "-u", "mongo/main.py"]
EXPOSE 27017