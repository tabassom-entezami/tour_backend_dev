#!/bin/bash

APP_ENV=${APP_ENV:-production}

# Check if rabbit is up and running before starting the service.
until nc -z "${RABBIT_HOST:-rabbit}" "${RABBIT_PORT:-5672}"; do
  echo "$(date) - waiting for rabbitmq..."
  sleep 2
done

if [[ "$APP_ENV" == "local" ]]; then
  echo "****************In local environment**************"

  # install shared from local
  if [ -d /shared/ ]; then
    echo "installing local shared library ..."
    pip install -e /shared/
  fi

  # Check requirements.
  which inotifywait || apt -qq install --yes inotify-tools
  which ps || apt -qq install --yes procps

  nameko run --config config.yml processor.controller --backdoor-port 3000
else
  exec nameko run --config config.yml processor.controller --backdoor-port 3000
fi
