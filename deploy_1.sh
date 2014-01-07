#!bin/bash

#just update server
sudo apt-get update
sudo apt-get upgrade

#postgres part
sudo apt-get install postgresql postgresql-contrib
sudo su - postgres
createuser --no-superuser --no-createdb --no-createrole octopus_user
createdb --owner octopus_user db1
psql -U postgres -d db1 -c "alter user octopus_user with password 'e9IKyjFIRbDgGPumhyvOOKvGWuV8CPp1xkABMS8abV4p9bKUnO5g7WfCkdk4s1l';"
#connect to db using: psql -U octopus_user -h localhost db1

#install virtualenv
sudo mkdir /webapps
cd /webapps
sudo apt-get install python-virtualenv

