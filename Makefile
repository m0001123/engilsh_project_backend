#.PHONY: start

help: make-help

pull-master: git-pull-master wsgi-reload-master
start-master: wsgi-stop-master wsgi-start-master
reload-master: wsgi-reload-master
stop-master: wsgi-stop-master
view-log-master: wsgi-view-log-master

pull-develop: git-pull-develop wsgi-reload-develop
start-develop: wsgi-stop-develop wsgi-start-develop
reload-develop: wsgi-reload-develop
stop-develop: wsgi-stop-develop
view-log-develop: wsgi-view-log-develop


make-help:
	@echo "# make <功能> ..."

##### git 相關
git-pull-master:
	@echo "# 正在從 Git 上獲取最新檔案並覆蓋 ..."
	@echo "## 先取回遠端數據庫的最新歷史紀錄"
	@git fetch --all
	@echo "## 然後放棄目前所有檔案與 commit，還原成遠端版本"
	@git reset --hard origin/master
	@echo "## 最後重新拉回來"
	@git pull origin master
	@chmod 755 -R *
	@echo "# 已從 Git 上獲取最新檔案並覆蓋"
	@echo "# 環境安裝"
	@pipenv install
	@echo "# 已完成環境安裝"
##### wsgi 相關
wsgi-start-master:
	@echo "# wsgi 服務正在啟動 ..."
	@if [ -e /tmp/api-master.pid ]; then echo "# wsgi 服務已存在"; else pipenv run uwsgi --ini ./api/uwsgi.ini && echo "# wsgi 服務已啟動"; fi
wsgi-reload-master:
	@echo "# wsgi 服務正在重啟 ..."
	@if [ -e /tmp/api-master.pid ]; then pipenv run uwsgi --reload /tmp/api-master.pid && echo "# wsgi 服務已重啟"; else echo "# wsgi 服務未啟動"; fi
wsgi-stop-master:
	@echo "# wsgi 服務正在關閉 ..."
	@if [ -e /tmp/api-master.pid ]; then pipenv run uwsgi --stop /tmp/api-master.pid && echo "# wsgi 服務已關閉，等待五秒鐘 ..." && sleep 5; else echo "# wsgi 服務未啟動"; fi
wsgi-view-log-master:
	@echo "# 以下為 wsgi 服務的記錄檔 >>>>>>>>>>"
	@cat /var/log/uwsgi/api.alicsnet.com.log
	@echo "# 以上為 wsgi 服務的記錄檔 >>>>>>>>>>"


##### git 相關
git-pull-develop:
	@echo "# 正在從 Git 上獲取最新檔案並覆蓋 ..."
	@echo "## 先取回遠端數據庫的最新歷史紀錄"
	@git fetch --all
	@echo "## 然後放棄目前所有檔案與 commit，還原成遠端版本"
	@git reset --hard origin/develop
	@echo "## 最後重新拉回來"
	@git pull origin develop
	@chmod 755 -R *
	@echo "# 已從 Git 上獲取最新檔案並覆蓋"
	@echo "# 環境安裝"
	@pipenv install
	@echo "# 已完成環境安裝"
##### wsgi 相關
wsgi-start-develop:
	@echo "# wsgi 服務正在啟動 ..."
	@if [ -e /tmp/api-develop.pid ]; then echo "# wsgi 服務已存在"; else pipenv run uwsgi --ini ./api/uwsgi.ini && echo "# wsgi 服務已啟動"; fi
wsgi-reload-develop:
	@echo "# wsgi 服務正在重啟 ..."
	@if [ -e /tmp/api-develop.pid ]; then pipenv run uwsgi --reload /tmp/api-develop.pid && echo "# wsgi 服務已重啟"; else echo "# wsgi 服務未啟動"; fi
wsgi-stop-develop:
	@echo "# wsgi 服務正在關閉 ..."
	@if [ -e /tmp/api-develop.pid ]; then pipenv run uwsgi --stop /tmp/api-develop.pid && echo "# wsgi 服務已關閉，等待五秒鐘 ..." && sleep 5; else echo "# wsgi 服務未啟動"; fi
wsgi-view-log-develop:
	@echo "# 以下為 wsgi 服務的記錄檔 >>>>>>>>>>"
	@cat /var/log/uwsgi/api-develop.alicsnet.com.log
	@echo "# 以上為 wsgi 服務的記錄檔 >>>>>>>>>>"
