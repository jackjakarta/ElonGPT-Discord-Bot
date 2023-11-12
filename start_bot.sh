#!/bin/bash

. env/bin/activate

sleep 2

nohup python3 -u main.py &>> activity.log &

sleep 2

echo "Bot started in the background. Check 'activity.log' file for console output!"

curl -d "ElonGPT Bot is up and running!" 139-162-166-208.ip.linodeusercontent.com/coffee
