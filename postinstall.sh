cd server
pipenv install
DJANGO_SETTINGS_MODULE=mahjong_statboard.settings_prod
python manage.py migrate

cd ../client
npm update
npm run build
cd ..
