#!/bin/bash

#my_ip=`curl -s http://checkip.dyndns.org | sed 's/[a-zA-Z/<> :]//g'`

# if need be, on new server, make ssh accesible from master to dev:
# ssh -i /Users/john-davidwuarin/Dropbox/Server_me/octopus/octopus_key ubuntu@octopus_postgres_master.baskettt.co
# ssh-keygen
# copy content of .ssh/id_rsa.pub from octopus master to end of ile .ssh/authorized_keys on portgres dev


# go to postgres_master
ssh -i /Users/john-davidwuarin/Dropbox/Server_me/octopus/octopus_key ubuntu@octopus_postgres_master.baskettt.co

sudo pg_dump db1 -U octopus_user --password -F t -h localhost > db_image.sql

# copy it from master to to dev
scp db_image.sql ubuntu@octopus_postgres_dev.baskettt.co:~

# actually kept on local. Use this file as a base when doing master/slave replication
# this command copies the dump_data from postgres_master to the local file
# scp -i /Users/john-davidwuarin/Dropbox/Server_me/octopus/octopus_key ubuntu@octopus_postgres_master.baskettt.co:db_image.sql ~

#actually get on postgres_dev and apply backup
exit
ssh -i /Users/john-davidwuarin/Dropbox/Server_me/octopus/octopus_key ubuntu@octopus_postgres_dev.baskettt.co

# restore data from file
sudo su postgresql
dropdb dev
createdb --owner octopus_user dev
pg_restore -U octopus_user -h localhost -d dev db_image.sql
exit
#sometimes useful to restart server.
#sudo service postgresql restart
exit