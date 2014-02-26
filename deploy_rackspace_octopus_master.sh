#!bin/bash

adduser ubuntu
sudo usermod -aG sudo ubuntu
su ubuntu
sudo passwd -l root

#copy ssh public key to server from LOCAL
scp ~/Dropbox/Server_me/octopus/octopus_key.pub ubuntu@134.213.31.177:/home/ubuntu/

#back on server:
mkdir /home/ubuntu/.ssh
mv /home/ubuntu/octopus_key.pub /home/ubuntu/.ssh
chown -R ubuntu:ubuntu /home/ubuntu/.ssh
chmod 700 /home/ubuntu/.ssh
chmod 600 /home/ubuntu/.ssh/authorized_keys
 
# make sure this file: "/etc/ssh/sshd_config"
# contains the following:
Protocol 2
PermitRootLogin no
PasswordAuthentication no
UseDNS no
AllowUsers ubuntu

# setup iptables (create rules)
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -I INPUT -p tcp  --dport 22 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -j DROP
sudo iptables -I INPUT 1 -i lo -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables.up.rules

# make iptables reload everytime we restart the server
sudo touch /etc/network/if-pre-up.d/iptables
echo '#!/bin/sh' | sudo tee -a /etc/network/if-pre-up.d/iptables
echo '/sbin/iptables-restore < /etc/iptables.up.rules' | sudo tee -a /etc/network/if-pre-up.d/iptables
sudo chmod +x /etc/network/if-pre-up.d/iptables

# save changes made to iptables on shutdown
sudo touch /etc/network/if-post-down.d/iptables
echo '#!/bin/sh
iptables-save -c > /etc/iptables.save
if [ -f /etc/iptables.downrules ]; then
   iptables-restore < /etc/iptables.downrules
fi
exit 0' | sudo tee -a /etc/network/if-post-down.d/iptables

sudo service ssh restart

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
cd webScraper/
scrapy crawl tesco
scrapy crawl food_com
scrapy crawl abs_prod_prod_match

#dealing with gunicorn
sudo chown -R octopus:users ./ #just making sure the privileges are still acurate
cp gunicorn_start.sh ./env/bin
sudo chown octopus:users ./env/bin/gunicorn_start.sh
sudo chmod u+x ./env/bin/gunicorn_start.sh
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