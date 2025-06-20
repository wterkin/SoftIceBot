#!/bin/sh
cd ~/
touch flags/start.flg
yes | rm /home/softice/logs/output.log
screen -L -Logfile logs/output.log -d -m ./bot_start.sh 

