#!/bin/bash



source ./services/flask_admin/venv/bin/activate

set -o allexport
source .env.dev
set +o allexport

docker-compose up -d

# sleep 10

# echo will create db
# python3 ./services/flask_admin/manage.py create_db
# echo db created

python3 ./services/flask_admin/manage.py run -h 0.0.0.0
