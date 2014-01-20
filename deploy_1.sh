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
psql -U octopus_user db1 -c 'create extension hstore;'
psql -U octopus_user db1 -c 'create extension unaccent;'
psql -U octopus_user db1 -c 'alter function unaccent(text) immutable;'
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

#populating the db
python manage.py schemamigration 'octopus_groceries' --initial
python manage.py schemamigration 'octopus_user' --initial
echo "no" | python manage.py syncdb #don't create superuser
python manage.py createsuperuser --noinput --email webmaster@baskettt.co --username django_auth_user
python manage.py migrate 'octopus_groceries'
python manage.py migrate 'octopus_user'
python manage.py loaddata supermarket_fixture.json
cd webScraper/
scrapy crawl tesco
scrapy crawl food_com
scrapy crawl abs_prod_prod_match

#elasticsearch
sudo apt-get update
sudo apt-get install openjdk-7-jre-headless -y
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.10.deb
sudo dpkg -i elasticsearch-0.90.10.deb
#then run elasticsearch (find out how to do that safely)

#haystack
#nothing to do really, all covered in code if not:
#python manage.py update_index #to build the index (do after db population)

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
sudo cp ./octopus.conf /etc/supervisor/conf.d/octopus.conf
sudo supervisorctl update
#sudo supervisorctl stop|start|restart octopus  #to do stuff to process

#nginx
sudo apt-get install -y nginx
sudo cp ./octopus_nginx.conf /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/octopus_nginx.conf /etc/nginx/sites-enabled

#ssl stuff
#make sure the certificates are on the server, say in /home/ubuntu
# sudo mv /home/ubuntu/baskettt.co_2014_ssl_cert.pem /etc/ssl/certs
# sudo mv /home/ubuntu/baskettt.co_2014_ssl_key.key /etc/ssl/private
# sudo chown root:root /etc/ssl/certs/baskettt.co_2014_ssl_cert.pem /etc/ssl/private/baskettt.co_2014_ssl_key.key
# sudo chmod 600 /etc/ssl/certs/baskettt.co_2014_ssl_cert.pem /etc/ssl/private/baskettt.co_2014_ssl_key.key
















