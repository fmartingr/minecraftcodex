#!/bin/bash

# CONFIG
WORKERS=2
SETTINGS="herobrine.local_settings"

# Get environment resources
source .bash_profile
source virtualenv/bin/activate

# Start
gunicorn_django app --settings=$SETTINGS -w $WORKERS
