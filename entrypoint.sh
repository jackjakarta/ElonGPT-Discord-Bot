#!/bin/bash

tail -f /dev/null &
TAIL_PID=$!
cd /root/ElonGPT-Discord-Bot/
git pull
source env/bin/activate
pip3 install --upgrade -r requirements.txt
nohup python3 main.py > activity.log 2>&1 &
trap "kill $TAIL_PID" EXIT
wait
