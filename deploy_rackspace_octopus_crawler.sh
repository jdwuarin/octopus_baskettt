#!bin/bash

#just update server
sudo apt-get update
sudo apt-get -y upgrade

#clone project
sudo apt-get install -y git
sudo apt-get install -y rabbitmq-server
git config --global user.name "john-dwuarin"
sudo mkdir /webapps
cd /webapps
sudo git clone https://john-dwuarin:st4bV3rr3@github.com/arnaudbenard/octopus.git

#create octopus user
sudo groupadd --system webapps
sudo useradd --system --gid webapps --home /webapps/octopus octopus
sudo chown -R octopus:users /webapps/octopus
sudo usermod -a -G users ubuntu #just makes ubuntu have r/w access to octopus folder
newgrp users #making sure group is loaded for ubuntu user
sudo chmod -R g+w /webapps/octopus

#install virtualenv
sudo apt-get install python-virtualenv
cd /webapps/octopus
virtualenv env
source ./env/bin/activate
sudo apt-get install -y libpq-dev python-dev libxml2-dev libxslt-dev gcc
pip install -r stable-req.txt

#populating the db
python manage.py syncdb
python manage.py migrate
python manage.py loaddata supermarket_fixture.json
python manage.py loaddata invited_users_fixture.json
python manage.py loaddata diet_fixture.json
python manage.py loaddata bannable_meats_fixture.json
python manage.py loaddata tag_fixtures.json # must be run before food_com spider
python manage.py loaddata django_sites.json
python manage.py loaddata fixtures/django_sites.json

cd webScraper/
scrapy crawl tesco
scrapy crawl food_com
scrapy crawl abs_prod_prod_match

#haystack
#nothing to do really, all covered in code if not:
#python manage.py update_index #to build the index (do after db population)

#rabbitmq
cd ../
sudo apt-get install rabbitmq-server # this should also start the rabbitmq server
sudo rabbitmqctl add_user octopus_rabbitmq_user octopus_rabbitmq_password
sudo rabbitmqctl add_vhost octopus_rabbitmq_vhost
sudo rabbitmqctl set_permissions -p octopus_rabbitmq_vhost octopus_rabbitmq_user ".*" ".*" ".*"

# sudo rabbitmq-server -detached #if rabbitmq server not running

#celery/

sudo apt-get install -y supervisor
mkdir -p /webapps/octopus/env/logs/celery
touch /webapps/octopus/env/logs/celery/beat.log
sudo chown -R octopus:users /webapps/octopus/env/logs
sudo cp ./octopus_cron_jobs.conf /etc/supervisor/conf.d/octopus_cron_jobs.conf
sudo supervisorctl update
#sudo supervisorctl stop|start|restart octopus_cron_jobs  #to do stuff to process

