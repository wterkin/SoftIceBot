#~/bin/env/bin/python3 test_softice.py -v
clear
touch flags/unittest.flg
# ~/bin/env/bin/python3 -m unittest test_softice.py -vv
~/bin/env/bin/python3 -m unittest tests/* -vv
# >unittest.log 2>unittest2.log
# rm flags/unittest.flg
# cat unittest2.log
#cat unittest.log
read 5