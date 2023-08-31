#!/bin/bash

if [[ "${1}" == "worker" ]]; then
    if [[ "${2}" == "clear_db" ]]; then
      celery --app=app.tasks:celery worker -l INFO -Q clear_db
    elif [[ "${2}" == "check_ids" ]]; then
      celery --app=id_generator.tasks:celery worker -l INFO -Q check_ids
    fi
elif [[ "${1}" == "beat" ]]; then
    if [[ "${2}" == "clear_db" ]]; then
      celery --app=app.tasks:celery beat -l INFO
    elif [[ "${2}" == "check_ids" ]]; then
      celery --app=id_generator.tasks:celery beat -l INFO
    fi
fi