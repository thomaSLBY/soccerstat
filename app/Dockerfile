FROM python:3.8-slim
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]