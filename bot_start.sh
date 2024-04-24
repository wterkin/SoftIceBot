#!/bin/bash
START_FLAG=~/softice/flags/start.flg
EXITING_FLAG=~/softice/flags/exiting.flg
CONDITION=0
cd ~/softice
if [ -e "$START_FLAG" ]
then

  rm $EXITING_FLAG
  rm $START_FLAG
  for ((CONDITION=0;CONDITION==0;)) do

    ~/env/telegram/bin/python3 softice.py
    if [ -e "$EXITING_FLAG" ]
    then

      echo **** Exiting.. ****
      break
    fi
  done
fi
