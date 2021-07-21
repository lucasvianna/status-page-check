FROM alpine:3.14

RUN apk update && apk add --no-cache python3 py3-pip python3-dev \
  gcc libxml2 libxml2-dev libxslt libxslt-dev libc-dev \
  libffi libffi-dev bash build-base rust
RUN pip3 install --upgrade pip 

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt
COPY . ./
EXPOSE 5000

# ENTRYPOINT ["python3","status-page-check.py"]
CMD ["bash","scripts/server.sh"]
