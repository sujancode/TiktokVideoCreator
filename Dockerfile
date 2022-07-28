# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/playwright

RUN apt update
RUN apt install python3-pip -y

ENV REDDIT_CLIENT_SECRET=Hlxm8t9vt3urxzMA5z9wFChs2SuzJQ
ENV REDDIT_CLIENT_ID=slMF0ZyjVVzb4g7BovHuGQ
ENV REDDIT_USERNAME=tiktok_view_maker
ENV REDDIT_PASSWORD=Earning$$
ENV AWSAccessKeyId=AKIARQCFY36WFTAC74VA
ENV AWSSecretKey=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

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

COPY . .
CMD ["python3","-u","manage.py","runserver","0.0.0.0:8080"]