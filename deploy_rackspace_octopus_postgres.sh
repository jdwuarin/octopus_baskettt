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
sudo iptables -I INPUT -p tcp  --dport 22 -j ACCEPT # add ip from octopus_master and slave etc...
sudo iptables -I INPUT -p tcp  --dport 5432 -j ACCEPT # postgres port
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

#postgres part
sudo apt-get install postgresql postgresql-contrib
sudo su - postgres
createuser --no-superuser --no-createdb --no-createrole octopus_user
createdb --owner octopus_user db1
psql -U postgres -d db1 -c "alter user octopus_user with password 'e9IKyjFIRbDgGPumhyvOOKvGWuV8CPp1xkABMS8abV4p9bKUnO5g7WfCkdk4s1l';"
psql -U postgres db1 -c 'create extension hstore;'
psql -U postgres db1 -c 'create extension unaccent;'
psql -U postgres template1 -c 'create extension hstore;'
psql -U postgres template1 -c 'create extension unaccent;'
exit #of postgres
#connect to db using: psql -U octopus_user -h localhost db1
