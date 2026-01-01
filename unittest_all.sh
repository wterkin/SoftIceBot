#~/bin/env/bin/python3 test_softice.py -v
clear
touch flags/unittest.flg
/home/app/bin/python/tg_env/bin/python3 -m unittest discover -s tests/ -p 'test*.py' -vv >unittest.log 2>unittest2.log
