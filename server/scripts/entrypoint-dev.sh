#!/bin/bash

DEFAULT_MODULE_NAME=src.asgi

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-application}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8100}
LOG_LEVEL=${LOG_LEVEL:-info}
LOG_CONFIG=${LOG_CONFIG:-/app/server/logging.ini}

# # Проверяем, были ли миграции выполнены
# if [ ! -f /app/server/scripts/migrations_done ]; then
#     /app/server/scripts/migrations.sh
#     touch /app/server/scripts/migrations_done
# fi

# # Проверяем, был ли createsuperuser выполнен
# if [ ! -f /app/server/scripts/createsuperuser_done ]; then
#     /app/server/scripts/createsuperuser.sh
#     touch /app/server/scripts/createsuperuser_done
# fi

/app/server/scripts/migrations.sh
/app/server/scripts/createsuperuser.sh

/opt/venv/bin/uvicorn --reload --proxy-headers --host $HOST --port $PORT --log-config $LOG_CONFIG "$APP_MODULE"
