#!/bin/bash

poetry run python /app/check_conn.py --service-name db --port 5432  --ip db --check_db 1
poetry run python /app/check_conn.py --service-name rabbit --port 5672  --ip rabbit


if [ $RUN_TEST ]
then
cd app
poetry run python -m pytest .
exit $?
fi


poetry run alembic upgrade head

cd app

poetry run uvicorn main:app --reload --host $HOST --port $PORT