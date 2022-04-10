#!/bin/bash

cd api

pipenv run uwsgi --ini uwsgi.ini

exit 0
