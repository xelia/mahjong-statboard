#!/bin/bash

cd server
PIPENV_VENV_IN_PROJECT=1
pipenv install
DJANGO_SETTINGS_MODULE=mahjong_statboard.settings_prod
pipenv run python manage.py migrate

cd ../client
npm update
npm run build
cd ..
