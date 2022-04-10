# api.alicsnet.com

## 結構
```
./
├── Pipfile # pipenv 的環境設定
├── README.md
├── api/ # Django 程式資料夾
├── pull_and_restart.sh # 從 Github master 分支上覆蓋到本地，並且重新啟動 uwsgi 服務
└── start.sh # 啟動 Django <->uwsgi 服務
```