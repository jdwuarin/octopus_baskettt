# make sure this file: "/etc/ssh/sshd_config"
# contains the following:
AllowUsers ubuntu postgres

#just update server
sudo apt-get update
sudo apt-get -y upgrade

#postgres part
sudo apt-get install -y postgresql postgresql-contrib postgresql-client
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

# add postgres port to iptables
sudo iptables -I INPUT 1 -p tcp  --dport 5435 -j DROP # postgres port
sudo iptables -I INPUT 1 -p tcp -s 162.13.176.229 --dport 5435 -j ACCEPT # add similar line for all that can connect here
sudo iptables -I INPUT 1 -p tcp -s 134.213.31.177 --dport 5435 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp -s 162.13.177.208 --dport 5435 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp -s 127.0.0.1 --dport 5435 -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables.up.rules

# add to /etc/postgresql/9.1/main/pg_hba.conf something like
host    db1             octopus_user    0.0.0.0/0       md5


# make sure /etc/postgresql/9.1/main/postgresql.conf contains:
listen_addresses = '*'
port = 5435


