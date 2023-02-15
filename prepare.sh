
python3 -m venv ./services/flask_admin/venv

source ./services/flask_admin/venv/bin/activate

pip3 install -r ./services/flask_admin/requirements.txt

set -o allexport
source .env.dev
set +o allexport

docker-compose up -d

sleep 10

python3 ./services/flask_admin/manage.py create_db