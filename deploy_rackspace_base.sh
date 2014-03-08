#!bin/bash

#first
apt-get update
apt-get install -y vim htop screen
adduser --disabled-password --gecos "" ubuntu
usermod -aG sudo ubuntu
echo "ubuntu ALL=(ALL) NOPASSWD: ALL" | tee -a /etc/sudoers
su ubuntu
sudo passwd -l root

# deal with ssh nonesense
mkdir /home/ubuntu/.ssh
chmod 700 /home/ubuntu/.ssh
sudo cp /root/.ssh/authorized_keys /home/ubuntu/.ssh
sudo chown -R ubuntu:ubuntu /home/ubuntu/.ssh
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
sudo iptables -I INPUT 1 -p tcp  --dport 22 -j ACCEPT
sudo iptables -A INPUT -j DROP
sudo iptables -I INPUT 1 -i lo -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables.up.rules

# make iptables reload everytime we restart the server
sudo touch /etc/network/if-pre-up.d/iptables
echo '#!/bin/sh' | sudo tee -a /etc/network/if-pre-up.d/iptables
echo '/sbin/iptables-restore < /etc/iptables.up.rules' | sudo tee -a /etc/network/if-pre-up.d/iptables
sudo chmod +x /etc/network/if-pre-up.d/iptables

sudo service ssh restart
