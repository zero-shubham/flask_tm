FROM python:3.9.2-slim-buster

WORKDIR /home/tm

COPY ./tm/requirements.txt ./
RUN pip install -r requirements.txt
CMD ["celery","-A","tm.utils.celery.celery","beat","--loglevel=info"]
