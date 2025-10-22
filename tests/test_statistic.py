from unittest import TestCase
import json
from sys import platform
from pathlib import Path

import softice
import test_softice
import functions as func
import constants as cn
import database
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
        self.database: database.CDataBase = database.CDataBase(self.config, self.data_path)
        self.statistic: statistic.CStatistic = statistic.CStatistic(self.config, self.database)


    def test_extract_user_name(self):

        event: dict = {cn.MUSER_TITLE:"Andrey"}
        self.assertEqual(statistic.extract_user_name(event), "Andrey")
        event2: dict = {cn.MUSER_LASTNAME:"Petrovich"}
        self.assertEqual(statistic.extract_user_name(event2), " Petrovich")


    def test_add_chat_to_base(self):
        
        #add_chat_to_base(self, ptg_chat_id: int, ptg_chat_title: str):
        self.assertEqual(self.statistic.add_chat_to_base(777, "TestPlace"), 1)
        

    def tearDown(self):

        self.database.disconnect()
        for file in Path(self.data_path).glob("softice.db"):

            file.unlink()
