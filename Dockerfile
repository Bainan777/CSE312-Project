FROM python:3.8-slim-buster

ENV HOME /root
WORKDIR /root

COPY . .

# Download dependancies
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD  ["python", "server.py"]