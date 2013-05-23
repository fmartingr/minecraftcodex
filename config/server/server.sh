#!/bin/bash
set -e

LOGFILE=/home/app/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=1
USER=app
GROUP=app
SETTINGS="herobrine.settings"

cd /home/app
source .environment
source ./virtualenv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django app --settings=$SETTINGS -w $NUM_WORKERS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE
