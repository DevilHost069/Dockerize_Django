#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
     	   echo "inside loop waiting db ...."
	    sleep 60
    done

    echo "MySQL started and granting permissions ..."
   # mysql -u root --password="$MYSQL_ROOT_PASSWORD"  << EOF
  #  USE ${SQL_DATABASE};
 #   GRANT ALL PRIVILEGES ON *.* TO '${SQL_USER}';
#EOF
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"
