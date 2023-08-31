#!/bin/bash

gunicorn id_generator.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:7000