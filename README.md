[![Build Status](https://magnum.travis-ci.com/arnaudbenard/octopus.png?token=xzYsjD6yTXcExfozSfDg&branch=master)](https://magnum.travis-ci.com/arnaudbenard/octopus)

# Octopus

## How to use Grunt

Grunt is a front-end tool to compile the less to css and compress it.

`npm install grunt --save-dev`

`npm install`



`grunt production`



## How to use Bower

Package management for static libraries

`npm install -g bower`

`bower install`

## populating all dbs form scratch
```bash
createdb db1
psql
GRANT ALL PRIVILEGES ON DATABASE db1 to octopus_user;
python manage.py schemamigration 'octopusProducts' --initial
python manage.py syncdb -all

#when creating the django superuser upon frist calling "python manage.py syncdb"

create the superuser: yes
username: django_auth_user
email:
password: django_auth

#then to actually populate the dbs

cd webScraper/
scrapy crawl tesco
scrapy crawl food_com
scrapy crawl ing_prod_match
```

add the following to local settings: 

DATABASES = {
    'default': {
        'ENGINE': 'django_hstore.postgresql_psycopg2',  # Add 'postgresql_psycopg2'
        'NAME': 'db1',

        'USER': 'octopus_user',
        'PASSWORD': 'e9IKyjFIRbDgGPumhyvOOKvGWuV8CPp1xkABMS8abV4p9bKUnO5g7WfCkdk4s1l',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',           # Set to empty string for default.
    }
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',  # currently running locally
        'INDEX_NAME': 'haystack',
        'INCLUDE_SPELLING': True,
        'TIMEOUT': 120,
    },
}

Installing fortran compiler

brew install gfortran
