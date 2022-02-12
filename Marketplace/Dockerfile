# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/Marketplace

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install mysql dependencies
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev
RUN pip install -r requirements.txt
RUN apk del .tmp

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/Marketplace/entrypoint.sh
RUN chmod +x /usr/src/Marketplace/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/Marketplace/entrypoint.sh"]
