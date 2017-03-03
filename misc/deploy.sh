#!/bin/bash

if [ $# -eq 0 ]
then
	   echo "No branch name supplied"
	   exit 1
fi

echo "Stopping service …"
sudo systemctl stop members

echo "Generating backups of previous install …"
cp -rf ~/members ~/members_back

echo "Upgrading to last version …"
cd ~/members
git checkout ${args[0]}
git pull

echo "Running install procedure …"
rm -rf venv
virtualenv -p $(which python3) venv
source venv/bin/activate
pip install -r requirements.txt
bundle install --path=venv/ruby

echo "Running migration …"
python manage.py migrate

echo "Collecting static files …"
python manage.py collectstatic --noinput

echo "Restarting service …"
sudo systemctl restart members
sudo systemctl status members
