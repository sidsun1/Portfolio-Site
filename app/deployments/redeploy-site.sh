#!/bin/bash

cd /root/Portfolio-Site

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt

sudo systemctl restart myportfolio
