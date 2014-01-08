#!bin/bash

#just update server
sudo apt-get update
sudo apt-get -y upgrade

#postgres part
sudo apt-get install postgresql postgresql-contrib
sudo su - postgres
createuser --no-superuser --no-createdb --no-createrole octopus_user
createdb --owner octopus_user db1
psql -U postgres -d db1 -c "alter user octopus_user with password 'e9IKyjFIRbDgGPumhyvOOKvGWuV8CPp1xkABMS8abV4p9bKUnO5g7WfCkdk4s1l';"
exit #of postgres
#connect to db using: psql -U octopus_user -h localhost db1

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
sudo virtualenv env
source ./env/bin/activate
apt-get install -y libpq-dev python-dev libxml2-dev libxslt-dev
pip install -r stable-req.txt


#static assets
sudo apt-get update
sudo apt-get install -y python-software-properties python g++ make
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
sudo npm install -g grunt-cli
sudo su - octopus -c 'npm install'
sudo  npm install -g bower
sudo su - octopus -c 'bower install'
sudo su - octopus -c 'grunt production'

#populating de db
python manage.py schemamigration 'octopusProducts' --initial
echo "no" | python manage.py syncdb #don't create superuser
python manage.py createsuperuser --noinput --email foo@baskettt.co --username django_auth_user
python manage.py migrate 'octopusProducts'
cd webScraper/
scrapy crawl tesco
scrapy crawl food_com
scrapy crawl ing_prod_match

#dealing with gunicorn
cd ../
sudo chown -R octopus:users ./ #just making sure the privileges are still acurate
cp gunicorn_start.sh ./env/bin
sudo chown octopus:users ./env/bin/gunicorn_start.sh
chmod u+x ./env/bin/gunicorn_start.sh
sudo apt-get install python-dev
pip install setproctitle

#monitoring with supervisor
sudo apt-get install -y supervisor
mkdir -p /webapps/octopus/env/logs
touch /webapps/octopus/env/logs/gunicorn_supervisor.log 
sudo chown -R octopus:users /webapps/octopus/env/logs
cp ./ocotpus.conf /etc/supervisor/conf.d/octopus.conf





