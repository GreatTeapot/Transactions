FROM python:latest



RUN mkdir /test_project

WORKDIR /test_project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


RUN chmod a+x /test_project/docker/app.sh
