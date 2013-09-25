#!/bin/bash
 
NAME="octopus"                                  # Name of the application
DJANGODIR=/home/ubuntu/octopus         # Django project directory
SOCKFILE=/home/ubuntu/octopus/run/gunicorn.sock       # we will communicate using this unix socket
USER=ubuntu                                       # the user to run as
GROUP=ubuntu                                      # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=settings             # which settings file should Django use
DJANGO_WSGI_MODULE=wsgi                     # WSGI module name
 
echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR
source /home/ubuntu/octopus/env/bin/activate
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
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE
