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

first_run: bool = True

class CTestStatistic(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]
        self.database: db.CDataBase = db.CDataBase(self.config, self.data_path)
        global first_run    
        if first_run:

            for file in Path(self.data_path).glob("softice.db"):

               file.unlink()
            file_name =  Path(self.data_path) / "softice.db"
            if not file_name.is_file():

                print("Create!")
                self.database.create()
            first_run = False    
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


    def test_get_chat_id(self):

        # FixMe: Этот тест отрабатывает через раз
        self.assertEqual(self.statistic.get_chat_id(777), 1)
        self.assertEqual(self.statistic.get_chat_id(0), -1)
        

    def test_get_help(self):

        self.assertIn("перв10, перв25, перв50, личные", self.statistic.get_help(test_softice.TESTPLACE_CHAT_NAME))


    def test_get_hint(self):

        self.assertIn("стат, stat", self.statistic.get_hint(test_softice.TESTPLACE_CHAT_NAME))


    def test_save_all_type_of_messages(self):

        #    def save_all_type_of_messages(self, pevent: dict):
        pass



    def test_get_personal_information(self):
        
        # def get_personal_information(self, ptg_chat_id: int, puser_title: str):
        self.assertIn("наболтал", self.statistic.get_personal_information(777, "Master"))
        self.assertEqual(self.statistic.get_personal_information(777, "Somebody"), "")
        self.assertEqual(self.statistic.get_personal_information(1, "Master"), "")


    def test_get_statistic(self):

        #  def get_statistic(self, ptg_chat_id: int, pcount: int, porder_by: int):
        pass        


    def tearDown(self):

        self.database.disconnect()
