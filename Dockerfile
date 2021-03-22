FROM python:3.9.2-slim-buster

WORKDIR /home/tm

COPY ./tm/requirements.txt ./
RUN pip install -r requirements.txt
CMD ["flask","run","-h","0.0.0.0"]

EXPOSE 5000