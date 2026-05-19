# Nextcloud Task Automation

Small Python automation runner for Nextcloud Deck tasks.

This repo intentionally does not implement Deck API calls directly. It invokes
[`nextcloud-deck-cli`](https://github.com/hacker-h/nextcloud-deck-cli) and stays
focused on automation loops, scheduling, metrics, and task rules.

# Getting started

Install or build `nextcloud-deck-cli` first. The automation service expects a
`deck` executable on `PATH`, or a custom path in `NEXTCLOUD_DECK_CLI`.

From a sibling checkout:

```bash
cd /Users/hacker/src/github.com/hacker-h/nextcloud-deck-cli
go build -o deck ./cmd/deck
export NEXTCLOUD_DECK_CLI="$PWD/deck"
```

Environment:

```bash
export NEXTCLOUD_BASE_URL="https://nextcloud.example.com"
export NEXTCLOUD_USERNAME="my-service-user-name"
export NEXTCLOUD_APP_PASSWORD="my-service-user-app-password"
export NEXTCLOUD_DECK_CLI="deck"
```

`NEXTCLOUD_PASSWORD` is also supported by `nextcloud-deck-cli`.
`NEXTCLOUD_HOSTNAME` remains supported for older deployments; new config should
use `NEXTCLOUD_BASE_URL`.

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

# Design

`main.py` owns the long-running loop and Prometheus exporter.

`nextcloud.py` is a thin CLI client wrapper. It shells out to:

```bash
deck board list --json
deck list list --board <id> --json
```

Future automations should add small intent-level functions to `nextcloud.py`
that invoke `deck` commands, instead of adding direct HTTP calls here. Examples:

- recurring-task creation: `deck card create`
- task movement: `deck card move`
- description updates: `deck card describe`
- checklist updates: `deck todo add|check|uncheck`

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
