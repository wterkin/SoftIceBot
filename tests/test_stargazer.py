from unittest import TestCase
import json
from sys import platform
from datetime import date
import softice
import test_softice
import functions as func
import constants as cn
import stargazer
import datetime as dtime

class CTestStarGazer(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]
            
        self.stargazer: stargazer.CStarGazer = stargazer.CStarGazer(self.config, self.data_path)


    def test_calculate_easter(self):

        self.assertEqual(stargazer.calculate_easter(2025), dtime.datetime(2025, 4, 20))


    def test_additional_inf(self):

        self.assertIn("Рождественский пост.", self.stargazer.additional_info(dtime.date(2025, 1, 6)))
        self.assertIn("Рождество.", self.stargazer.additional_info(dtime.date(2025, 1, 7)))
        self.assertIn("Святки.", self.stargazer.additional_info(dtime.date(2025, 1, 8)))
        self.assertIn("Сырная седмица.", self.stargazer.additional_info(dtime.date(2025, 2, 20)))
        self.assertIn("Страстная седмица.", self.stargazer.additional_info(dtime.date(2025, 4, 18)))
        self.assertIn("Пасха.", self.stargazer.additional_info(dtime.date(2025, 4, 20)))
        self.assertIn("Светлая седмица.", self.stargazer.additional_info(dtime.date(2025, 4, 21)))
        self.assertIn("Сплошная седмица", self.stargazer.additional_info(dtime.date(2025, 6, 12)))
        self.assertIn("Петров пост.", self.stargazer.additional_info(dtime.date(2025, 6, 20)))
        self.assertIn("Успенский пост.", self.stargazer.additional_info(dtime.date(2025, 8, 27)))


    def test_can_process(self):
        
        self.assertTrue(self.stargazer.can_process(test_softice.TESTPLACE_CHAT_NAME, '!пасха'))
        self.assertTrue(self.stargazer.can_process(test_softice.TESTPLACE_CHAT_NAME, '!нг'))
        self.assertFalse(self.stargazer.can_process('fakechat', '!день'))
        self.assertFalse(self.stargazer.can_process('empttychat', '!дата'))
        self.assertFalse(self.stargazer.can_process(test_softice.TESTPLACE_CHAT_NAME, '!кукабарра'))


    def test_get_help(self):

        self.assertIn("пасха, easter", self.stargazer.get_help(test_softice.TESTPLACE_CHAT_NAME))


    def test_get_hint(self):

        self.assertIn("календарь, кл", self.stargazer.get_hint(test_softice.TESTPLACE_CHAT_NAME))
    

    def test_is_enabled(self):

        self.assertFalse(self.stargazer.is_enabled("fakechat"))
        self.assertFalse(self.stargazer.is_enabled("emptychat"))
        self.assertTrue(self.stargazer.is_enabled(test_softice.TESTPLACE_CHAT_NAME))

    def test_stargazer(self):

        self.assertEqual(self.stargazer.stargazer(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"), "")
        self.assertIn("пасха, easter", self.stargazer.stargazer(test_softice.TESTPLACE_CHAT_NAME, "!календарь"))
        self.assertIn("20.04.2025", self.stargazer.stargazer(test_softice.TESTPLACE_CHAT_NAME, "!пасха 2025"))
        self.assertIn("Невозможно рассчитать", self.stargazer.stargazer(test_softice.TESTPLACE_CHAT_NAME, "!пасха в этом году"))
        now_date: date = date.today()
        self.assertIn(f"{now_date.day:02}/{now_date.month:02}", self.stargazer.stargazer(test_softice.TESTPLACE_CHAT_NAME, "!дата"))
        
