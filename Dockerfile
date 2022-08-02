# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/playwright

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_REGION=us-east-1

RUN apt update
RUN apt install python3-pip -y

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    AWS_REGION=$AWS_REGION
    
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

COPY . .
CMD ["python3","-u","manage.py","runserver","0.0.0.0:8080"]