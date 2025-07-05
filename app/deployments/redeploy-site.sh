#!/bin/bash

tmux kill-server

cd ..
git fetch && git reset origin/main --hard

cd ..
source python3-virtualenv/bin/activate
pip install -r requirements.txt

tmux new-session -d -s flask_server 'export FLASK_APP=app && flask run --host=0.0.0.0'
