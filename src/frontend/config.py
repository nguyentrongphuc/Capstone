import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

auth0_url='phucnguyen.us'
auth0_audience='phuc'
auth0_clientId='J804TumgtEPJ9Sr0MY6opWIu3SmgROM9'
auth0_callbackURL='http://127.0.0.1:3000/'