#!/bin/bash

. env/bin/activate

sleep 1

nohup python3 -u main.py &>> activity.log &

echo "Bot started in the background. Check 'activity.log' file for console output!"
