FROM alpine:3.14

RUN apk update && apk add --no-cache python3 py3-pip python3-dev \
  bash build-base

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt

COPY . /usr/src/app

EXPOSE 5000
# ENTRYPOINT ["python3","status-page-check.py"]
CMD ["bash","server.sh"]
