#!bin/bash


#just update server
sudo apt-get update
sudo apt-get -y upgrade

# add elasticsearch port to iptables
sudo iptables -I INPUT 1 -p tcp  --dport 9201 -j DROP # postgres port
sudo iptables -I INPUT 1 -p tcp -s 162.13.176.229 --dport 9201 -j ACCEPT # add similar line for all that can connect here
sudo iptables -I INPUT 1 -p tcp -s 134.213.31.177 --dport 9201 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp -s 162.13.177.208 --dport 9201 -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables.up.rules

#elasticsearch
sudo apt-get update
sudo apt-get install openjdk-7-jre-headless -y
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.10.deb
sudo dpkg -i elasticsearch-0.90.10.deb
sudo cp /home/ubuntu/elasticsearch.yml /etc/elasticsearch

