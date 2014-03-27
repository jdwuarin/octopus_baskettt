#!bin/bash

sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables.up.rules

sudo service ssh restart

#just update server
sudo apt-get update
sudo apt-get -y upgrade

#clone project
sudo apt-get install -y git
git config --global user.name "octopus_admin_server"
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
sudo apt-get -y install python-virtualenv
cd /webapps/octopus
virtualenv env
source ./env/bin/activate
sudo apt-get install -y libpq-dev python-dev libxml2-dev libxslt-dev gcc
pip install -r stable-req.txt

#static assets
sudo apt-get update
sudo apt-get install -y python-software-properties python g++ make
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get -y install nodejs
sudo npm install -g grunt-cli
sudo su - octopus -c 'npm install'
sudo npm install -g bower
sudo su - octopus -c 'bower install'
sudo su - octopus -c 'grunt production'

#dealing with gunicorn
sudo chown -R octopus:users ./ #just making sure the privileges are still acurate
ln gunicorn_start.sh ./env/bin # not a symbolic link
sudo chmod u+x ./env/bin/gunicorn_start.sh
sudo apt-get install python-dev

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