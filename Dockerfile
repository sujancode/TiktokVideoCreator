# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/playwright

RUN apt update
RUN apt install python3-pip -y



WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

COPY . .
CMD ["python3","-u","manage.py","runserver","0.0.0.0:8080"]