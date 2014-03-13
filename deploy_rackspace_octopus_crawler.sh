#!bin/bash

#just update server
sudo apt-get update
sudo apt-get -y upgrade

#clone project
sudo apt-get install -y git
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
python manage.py schemamigration 'octopus_groceries' --initial
python manage.py schemamigration 'octopus_user' --initial
echo "no" | python manage.py syncdb #don't create superuser
python manage.py createsuperuser --noinput --email webmaster@baskettt.co --username django_auth_user
python manage.py migrate 'octopus_groceries'
python manage.py migrate 'octopus_user'
python manage.py loaddata supermarket_fixture.json
python manage.py loaddata invited_users_fixture.json
python manage.py loaddata diet_fixture.json
python manage.py loaddata bannable_meats_fixture.json
python manage.py loaddata tag:fixtures.json # must be run before food_com spider
cd webScraper/
scrapy crawl tesco
scrapy crawl food_com
scrapy crawl abs_prod_prod_match

#haystack
#nothing to do really, all covered in code if not:
#python manage.py update_index #to build the index (do after db population)