from unittest import TestCase
import json
from sys import platform
from pathlib import Path

import softice
import test_softice
import functions as func
import constants as cn
import database as db
import statistic
import datetime as dtime

class CTestStatistic(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]
        self.database: db.CDataBase = db.CDataBase(self.config, self.data_path)
        self.database.create()
        self.statistic: statistic.CStatistic = statistic.CStatistic(self.config, self.database)


    def test_extract_user_name(self):

        event: dict = {cn.MUSER_TITLE:"Andrey"}
        self.assertEqual(statistic.extract_user_name(event), "Andrey")
        event2: dict = {cn.MUSER_LASTNAME:"Petrovich"}
        self.assertEqual(statistic.extract_user_name(event2), " Petrovich")


    def test_add_chat_to_base(self):
        
        self.assertEqual(self.statistic.add_chat_to_base(777, "TestPlace"), 1)
        

    def test_add_user_to_base(self):

        self.assertEqual(self.statistic.add_user_to_base(777, "Master"), 1)
        


    def test_add_user_stat(self):

        statfields: dict = {db.STATUSERID: 0,
                            db.STATLETTERS: 2,
                            db.STATWORDS: 3,
                            db.STATPHRASES: 4,
                            db.STATPICTURES: 5,
                            db.STATSTICKERS: 6,
                            db.STATAUDIOS: 7,
                            db.STATVIDEOS: 8}
        self.assertEqual(self.statistic.add_user_stat(1, 1, statfields), 1)


    def test_can_process(self):

        self.assertFalse(self.statistic.can_process("fakechat", "!top10"))
        self.assertFalse(self.statistic.can_process("emptychat", "!top10"))
        self.assertTrue(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!top10"))
        self.assertTrue(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!top25"))
        self.assertTrue(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!top50"))
        self.assertTrue(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!pers"))
        self.assertTrue(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!перв10"))
        self.assertTrue(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!перв25"))
        self.assertTrue(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!перв50"))
        self.assertTrue(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!личные"))
        self.assertFalse(self.statistic.can_process(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"))



    def tearDown(self):

        self.database.disconnect()
        for file in Path(self.data_path).glob("softice.db"):

            file.unlink()
