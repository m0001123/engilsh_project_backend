#!/bin/bash

git fetch origin
git pull --force origin master

pipenv run uwsgi --reload /tmp/api-master.pid

exit 0