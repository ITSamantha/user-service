FROM python:3.10-alpine
WORKDIR /app

COPY . .
COPY ./entrypoint.sh entrypoint.sh

RUN apk update \
    && apk add \
           build-base \
           linux-headers \
           python3-dev \
           musl-dev && \
    pip install -r requirements/base.txt

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["sh", "entrypoint.sh"]