#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "### Aguardando pelo inicio do Postgres Database($POSTGRES_HOST $POSTGRES_PORT) ###"
    sleep 2
done

echo "@@@ Database iniciado com sucesso($POSTGRES_HOST:$POSTGRES_PORT) @@@"

python3 manage.py collectstatic --noinput
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8000
