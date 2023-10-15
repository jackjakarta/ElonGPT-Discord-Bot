#!/bin/bash

. env/bin/activate

sleep 2

nohup python3 -u main.py &>> activity.log &
