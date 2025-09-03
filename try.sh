#!/bin/bash
rm flags/unittest.flg
touch flags/try.flg
~/bin/env/bin/python3 softice.py
rm flags/try.flg
