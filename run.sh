#!/bin/sh
cd ~/softice
screen -Logfile ~/bot_screen.log -L -d -m ./bot_start.sh
ps ax | grep screen