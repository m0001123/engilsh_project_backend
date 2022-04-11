#!/bin/bash

#先取回遠端數據庫的最新歷史紀錄
git fetch --all 
#然後放棄目前所有檔案與 commit，還原成遠端版本
git reset --hard origin/master
#最後重新拉回來
git pull origin master

chmod 755 -R *

# 防止重啟 uwsgi 後 Memory Leak
killall -9 java

# 重啟 uwsgi 服務
pipenv run uwsgi --reload /tmp/api-master.pid

exit 0