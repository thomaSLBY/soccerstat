FROM python:3.8-slim
ADD . /scraping
WORKDIR /scraping
RUN pip3 install -r requirements.txt
CMD ["python", "-u", "main.py"]
EXPOSE 8080