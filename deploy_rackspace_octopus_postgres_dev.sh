# done already from postgres master image

sudo su - postgres
createuser --no-superuser --no-createdb --no-createrole octopus_user
createdb --owner octopus_user dev
psql -U postgres -d dev -c "alter user octopus_user with password 'kABMS8abV4p9bKUnOFIRPp1x5g7WfCkdk4s1le9IKyjbDgGPumhyvOOKvGWuV8C';"
psql -U postgres dev -c 'create extension unaccent;'
psql -U postgres template1 -c 'create extension hstore;'
psql -U postgres template1 -c 'create extension unaccent;'

# add to /etc/postgresql/9.1/main/pg_hba.conf something like
host    dev             octopus_user    0.0.0.0/0       md5

# make sure /etc/postgresql/9.1/main/postgresql.conf contains:
listen_addresses = '*'
port = 5435