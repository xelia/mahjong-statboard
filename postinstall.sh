#!/bin/bash

cd server
export PIPENV_VENV_IN_PROJECT=1
pipenv install
export DJANGO_SETTINGS_MODULE=mahjong_statboard.settings_prod
pipenv run python manage.py migrate

cd ../client
npm update
npm run build
cd ..

sudo supervisorctl restart mahjong_statboard
