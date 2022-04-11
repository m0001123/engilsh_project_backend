#.PHONY: start

pull: git-pull wsgi-reload
start: wsgi-stop wsgi-start
reload: wsgi-reload
stop: wsgi-stop
view-log: wsgi-view-log

##### git 相關
git-pull:
	@echo "# 正在從 Git 上獲取最新檔案並覆蓋 ..."
	@echo "## 先取回遠端數據庫的最新歷史紀錄"
	@git fetch --all
	@echo "## 然後放棄目前所有檔案與 commit，還原成遠端版本"
	@git reset --hard origin/master
	@echo "## 最後重新拉回來"
	@git pull origin master
	@chmod 755 -R *
	@echo "# 已從 Git 上獲取最新檔案並覆蓋"
##### wsgi 相關
wsgi-start:
	@echo "# wsgi 服務正在啟動 ..."
	@pipenv run uwsgi --ini ./api/uwsgi.ini
	@echo "# wsgi 服務已啟動"
wsgi-reload:
	@echo "# wsgi 服務正在重啟 ..."
	@pipenv run uwsgi --reload /tmp/api-master.pid
	@echo "# wsgi 服務已重啟"
wsgi-stop:
	@echo "# wsgi 服務正在關閉 ..."
	@if [ -e /tmp/api-master.pid ]; then pipenv run uwsgi --stop /tmp/api-master.pid; fi
	@echo "# wsgi 服務已關閉"
	@echo "## 等待五秒 ..."
	@sleep 5
wsgi-view-log:
	@echo "# 以下為 wsgi 服務的記錄檔 >>>>>>>>>>"
	@cat /var/log/uwsgi/api.alicsnet.com.log
	@echo "# 以上為 wsgi 服務的記錄檔 >>>>>>>>>>"
