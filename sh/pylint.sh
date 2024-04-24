#!/bin/sh
if [ -e pylint.log ]
then
    rm pylint.log
fi
pylint --rcfile=~/.pylint.rc babbler.py > pylint.log
pylint --rcfile=~/.pylint.rc barman.py >> pylint.log
pylint --rcfile=~/.pylint.rc bellringer.py >> pylint.log
pylint --rcfile=~/.pylint.rc database.py >> pylint.log
pylint --rcfile=~/.pylint.rc debug.py >> pylint.log
pylint --rcfile=~/.pylint.rc functions.py >> pylint.log
pylint --rcfile=~/.pylint.rc haijin.py >> pylint.log
pylint --rcfile=~/.pylint.rc librarian.py >> pylint.log
pylint --rcfile=~/.pylint.rc majordomo.py >> pylint.log
pylint --rcfile=~/.pylint.rc messages.py >> pylint.log
pylint --rcfile=~/.pylint.rc meteorolog.py >> pylint.log
pylint --rcfile=~/.pylint.rc moderator.py >> pylint.log
pylint --rcfile=~/.pylint.rc softice.py >> pylint.log
pylint --rcfile=~/.pylint.rc stargazer.py >> pylint.log
pylint --rcfile=~/.pylint.rc statistic.py >> pylint.log
pylint --rcfile=~/.pylint.rc theolog.py >> pylint.log
cat pylint.log

