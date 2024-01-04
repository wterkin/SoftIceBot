#!/bin/bash
START_FLAG=~/softice/flags/start.flg
EXITING_FLAG=~/softice/flags/exiting.flg
CONDITION=0
cd ~/softice
if [ -e "$START_FLAG" ]
then

  # rm $START_FLAG
  #while [ $CONDITION -e 1 ] do
  for ((;$CONDITION==0;)) do
    ~/env/telegram/bin/python3 softice.py
    if [ -e "$EXITING_FLAG" ]
    then

      $CONDITION = 1

    fi

  done

fi
