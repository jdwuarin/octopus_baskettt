First step, get django up and running using a tunmbleblog example:

As I will be using mongodb, here it goes:

```shell
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 
$ echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list
$ sudo apt-get update
$ sudo apt-get install mongodb-10gen #this willl start mongodb automatically.
$ sudo apt-get install ipython python-pip
$ sudo apt-get install build-essential python-dev
$ sudo pip install virtualenv
```

Creating the virutal environment:

```shell
$ cd /home/john-d2/Dropbox/Workspace_Python
$ mkdir octopus
$ cd octopus
$ virutalenv env
$ source env/bin/activate
$ pip install gunicorn Django
$ pip install mongoengine
$ pip install djangotoolbox
$ django-admin.py startproject project
$ apt-get install libxml2-dev libxslt-dev
$ pip install Scrapy
$ pip install ipython
$ pip freeze > stable-req.txt #repeat whenever stable packages are udated
```

then actually getting started. Edit the settings.py file and add:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

```

In a python2 shell:

```python
from mongoengine import *

connect('tumblelog')
```

For the REST API:

```
pip install djangorestframework
pip install markdown
pip install django-filter
```

For Postgresql

```
sudo su - postgres
createdb db1
psql
CREATE USER octopus_user WITH PASSWORD 'octopus';
GRANT ALL PRIVILEGES ON DATABASE db1 to octopus_user;
curl http://nextmarvel.net/blog/downloads/fixBrewLionPostgres.sh | sh //if using Mac OSX Lion
```



Using south for ease of migration:

add 'south',

to INSTALLED_APPS in settings.py

do a "python manage.py syncdb" #this runs south syncdb
run a "python manage.py convert_to_south" on any app we have
Then if, say, a column was added to a model just: 

```
python manage.py schemamigration 'yourApp' --auto
python manage.py migrate 'yourApp'
```
Note: if we are creating a model we will need a first migration, we do that by: 

```
python manage.py schemamigration 'yourApp' --initial
python manage.py syncdb
python manage.py migrate 'yourApp'
```


For Django Users (and Auth...)

```
#when creating the django superuser upon frist calling "python manage.py syncdb"

create the superuser: yes
username: django_auth_user
email: 
password: django_auth

```
