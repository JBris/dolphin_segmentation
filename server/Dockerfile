ARG PYTHON_TAG

FROM python:${PYTHON_TAG}

WORKDIR /app
ADD . /app

RUN apt-get update && apt-get install -y python3-opencv

RUN pip install -r requirements.txt

EXPOSE 5000