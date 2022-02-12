#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 6
    done

    echo "MYSQL started"
fi

exec "$@"
