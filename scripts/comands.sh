#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "### Aguardando pelo inicio do Postgres Database($POSTGRES_HOST $POSTGRES_PORT) ###" &
    sleep 0.5
done

echo "@@@ Database iniciado com sucesso($POSTGRES_HOST:$POSTGRES_PORT) @@@"

python3 manage.py collectstatic
python3 manage.py migrate
python3 manage.py runserver
