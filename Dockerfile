FROM alpine:3.14

RUN apk update && apk add --no-cache python3 py3-pip python3-dev \
  gcc libxml2 libxml2-dev libxslt libxslt-dev libc-dev \
  libffi libffi-dev bash build-base rust
RUN pip3 install --upgrade pip 

COPY . ./

RUN pip3 install -r requirements.txt
EXPOSE 5000

# ENTRYPOINT ["python3","status-page-check.py"]
# ENTRYPOINT ["bash","scripts/server.sh"]
