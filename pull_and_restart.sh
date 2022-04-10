#!/bin/bash

#先取回遠端數據庫的最新歷史紀錄
git fetch --all 
#然後放棄目前所有檔案與 commit，還原成遠端版本
git reset --hard origin/master
#最後重新拉回來
git pull origin master

pipenv run uwsgi --reload /tmp/api-master.pid

exit 0