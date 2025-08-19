#~/bin/env/bin/python3 test_softice.py -v
clear
touch flags/unittest.flg
#~/bin/env/bin/python3 -m unittest tests/test_barman.py -vv
~/bin/env/bin/python3 -m unittest discover -s tests/ -p 'test_gambler.py' -vv >unittest.log 2>unittest2.log
# python -m unittest discover -s <directory> -p '*_test.py'
# 
# rm flags/unittest.flg
# cat unittest2.log
#cat unittest.log
# read 5