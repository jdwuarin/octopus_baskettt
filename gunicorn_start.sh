#!/bin/bash
 
NAME="octopus"                                  # Name of the application
DJANGODIR=/webapps/octopus         # Django project directory
SOCKFILE=/tmp/gunicorn.sock       # we will communicate using this unix socket
USER=octopus                                       # the user to run as
GROUP=webapps                                      # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=octopus.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=octopus.wsgi                     # WSGI module name
 
echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR
source ./env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

echo $PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
 
# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ./env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --log-level=debug \
  --bind=0.0.0.0:8000
