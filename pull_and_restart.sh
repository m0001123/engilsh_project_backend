#!/bin/bash

git pull

pipenv run uwsgi --reload /tmp/api-master.pid

exit 0
