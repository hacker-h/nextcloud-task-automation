# Nextcloud Task Automation

This is a small python webserver running queries against your nextcloud instance, specifically Nextcloud Deck.

# Getting started
```
# if you want to use a virtualenv
virtualenv -p python3 ~/.venv/nextcloud-task-automation
source ~/.venv/nextcloud-task-automation/bin/activate

# install dependencies
pip install -r requirements.txt

# prepare your .env file suitably
set -a
source .env

# launch the webserver
python main.py

# check your exported metrics
curl localhost:8000
```

# Features
- [x] read-only features
  - [x] count tasks per list per board
  - [x] board meta data prometheus exporter
- [ ] write-only features
  - [ ] cron based task creation
  - [ ] rule based task creation
  - [ ] event based task creation
- [ ] read-write features
  - [ ] move tasks between lists
  - [ ] task description updates
  - [ ] rule based task updates


# Potential Usecases
- automatic recreation of recurring tasks
- update broken links within tasks
- show old tasks
- inspect task metrics: total per list, created per day, etc.
- automatic archival of done tasks
- warning when total task number per board gets high (>200)
