#!/usr/bin/env bash
sudo apt-get install python-dev python-setuptools build-essential
sudo pip install -r requirements.txt
sudo -u postgres psql -U postgres -d postgres -c "CREATE DATABASE pythonappdb ENCODING 'UTF8' LC_COLLATE 'en_US.UTF-8' TEMPLATE template0;" && \
sudo -u postgres psql -U postgres -d pythonappdb -a -f pythonappdb.sql
sudo -u postgres psql -U postgres -d pythonappdb < constantes.sql