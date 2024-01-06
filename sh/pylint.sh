pylint --rcfile=~/.pylint.rc barman.py > pylint.log
pylint --rcfile=~/.pylint.rc functions.py >> pylint.log
pylint --rcfile=~/.pylint.rc librarian.py >> pylint.log
pylint --rcfile=~/.pylint.rc mafiozo.py >> pylint.log
pylint --rcfile=~/.pylint.rc meteorolog.py >> pylint.log
pylint --rcfile=~/.pylint.rc softice.py >> pylint.log
pylint --rcfile=~/.pylint.rc statistic.py >> pylint.log
pylint --rcfile=~/.pylint.rc theolog.py >> pylint.log
cat pylint.log

