# Octopus

## How to use Grunt

Grunt is a front-end tool to compile the less to css and compress it.
`npm install grunt --save-dev`
`npm install`
`grunt`

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
cd webscraper/
scrapy crawl tesco
scrapy crawl food_com
scrapy crawl ing_prod_match

