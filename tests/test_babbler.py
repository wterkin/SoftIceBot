import sys
from time import sleep
from unittest import TestCase
import json
import babbler
import uuid

import constants as cn
sys.path.insert(0, "tests/")
import test_softice
UNIT_CONFIG: str = "unittest_config.json"

class CTestBabbler(TestCase):

    def setUp(self) -> None:

        with open(UNIT_CONFIG, "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)

        self.babbler = babbler.CBabbler(self.config, self.config["linux_data_folder"])


    def test_babbler(self):

        event: dict = {}
        event[cn.MTEXT] = "!blreload"
        event[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        event[cn.MUSER_NAME] = self.config["master"]
        event[cn.MUSER_TITLE] = self.config["master_name"]
        self.assertEqual(self.babbler.babbler(event), "База болтуна обновлена")
        event[cn.MCHAT_TITLE] = "superchat"
        event[cn.MUSER_NAME] = "username"
        event[cn.MUSER_TITLE] = "usertitle"
        self.assertNotEqual(self.babbler.babbler(event), "База болтуна обновлена")


    def test_can_process(self):

        self.assertTrue(self.babbler.can_process(test_softice.TESTPLACE_CHAT_NAME, "!blreload"))
        self.assertFalse(self.babbler.can_process(test_softice.TESTPLACE_CHAT_NAME, "!day"))
        self.assertFalse(self.babbler.can_process("superchat", ""))


    def test_is_enabled(self):

        self.assertTrue(self.babbler.is_enabled(test_softice.TESTPLACE_CHAT_NAME))
        self.assertFalse(self.babbler.is_enabled("superchat"))


    def test_is_master(self):

        self.assertTrue(self.babbler.is_master(self.config["master"]))
        self.assertFalse(self.babbler.is_master("User"))


    def test_reload(self):

        self.assertTrue(self.babbler.reload())
        self.babbler.data_path = "./empty/"
        self.assertFalse(self.babbler.reload())


    def test_talk(self):

        sleep(int(self.babbler.config[babbler.BABBLER_PERIOD_KEY]))
        event: dict = {}
        event[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        event[cn.MTEXT] = 'Привет'
        self.assertEqual(self.babbler.talk(event), ("Здорово!", ""))
        event[cn.MTEXT] = 'Хай'
        self.assertEqual(self.babbler.talk(event), ("", ""))


    def test_think(self):

        event: dict = {}
        event[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        event[cn.MTEXT] = 'Спасибо, бот'
        self.assertEqual(self.babbler.think(event), ("Пожалуйста.", ""))
        event[cn.MTEXT] = 'Спасибо'
        self.assertEqual(self.babbler.think(event), ("", ""))
        # self.assertNotEqual(self.babbler.think('Привет'), "")
        # self.assertEqual(self.babbler.think('Кукареку'), "")

