# make sure this file: "/etc/ssh/sshd_config"
# contains the following:
AllowUsers ubuntu postgres

#just update server
sudo apt-get update
sudo apt-get -y upgrade

#partition the data disk
#xvde1 should already exist on /dev/xvde
sudo mkfs -t ext4 /dev/xvde1
sudo mkdir /mnt/data
sudo mount /dev/xvde1 /mnt/data
sudo chown -R postgres:postgres /mnt/data
sudo chmod -R 700 /mnt/data
echo "/dev/xvde1          /mnt/data              ext4    defaults,noatime,barrier=0 1 1" | sudo tee -a /etc/fstab

# be able to save data with rackspace backups
sudo sh -c 'wget -q "http://agentrepo.drivesrvr.com/debian/agentrepo.key" -O- | apt-key add -'
sudo sh -c 'echo "deb [arch=amd64] http://agentrepo.drivesrvr.com/debian/ serveragent main" > /etc/apt/sources.list.d/driveclient.list'
sudo apt-get update; sudo apt-get install driveclient
sudo /usr/local/bin/driveclient --configure # use key from rackspace
sudo service driveclient start
sudo update-rc.d driveclient defaults

#postgres part
sudo apt-get install -y postgresql postgresql-contrib postgresql-client

sudo pg_dropcluster --stop 9.1 main
sudo pg_createcluster -d /mnt/data 9.1 main
sudo service postgresql restart

sudo su - postgres
createuser --no-superuser --no-createdb --no-createrole octopus_user
createdb --owner octopus_user db1
psql -U postgres -d db1 -c "alter user octopus_user with password 'e9IKyjFIRbDgGPumhyvOOKvGWuV8CPp1xkABMS8abV4p9bKUnO5g7WfCkdk4s1l';"
psql -U postgres db1 -c 'create extension hstore;'
psql -U postgres db1 -c 'create extension unaccent;'
psql -U postgres template1 -c 'create extension hstore;'
psql -U postgres template1 -c 'create extension unaccent;'
exit #of postgres
#connect locally to db using: psql -U octopus_user -h localhost db1

# add to /etc/postgresql/9.1/main/pg_hba.conf something like
host    db1             octopus_user    0.0.0.0/0       md5


# make sure /etc/postgresql/9.1/main/postgresql.conf contains:
listen_addresses = '*'
port = 5435


# add postgres port to iptables
sudo iptables -I INPUT 1 -p tcp  --dport 5435 -j DROP # postgres port
sudo iptables -I INPUT 1 -p tcp -s octopus_crawler.baskettt.co --dport 5435 -j ACCEPT # add similar line for all that can connect here
sudo iptables -I INPUT 1 -p tcp -s octopus_master.baskettt.co --dport 5435 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp -s octopus_slave.baskettt.co --dport 5435 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp -s 127.0.0.1 --dport 5435 -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables.up.rules



