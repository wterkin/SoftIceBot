import sys
from time import sleep
from unittest import TestCase
import json
import babbler

sys.path.insert(0, "tests/")
import test_softice
UNIT_CONFIG: str = "unittest_config.json"

class CTestBabbler(TestCase):

    def setUp(self) -> None:

        with open(UNIT_CONFIG, "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)

        self.babbler = babbler.CBabbler(self.config, self.config["linux_data_folder"])


    def test_babbler(self):

        self.assertEqual(self.babbler.babbler(test_softice.TESTPLACE_CHAT_ID,
                                              self.config["master"],
                                              self.config["master_name"],
                                              "!blrl"), 'База болтуна обновлена')
        self.assertNotEqual(self.babbler.babbler('megachat', 'username', 'usertitle', '!reload'),
                            'База болтуна обновлена')

"""
    def test_can_process(self):
        self.assertEqual(self.babbler.can_process('superchat', ''), True)

    def test_is_enabled(self):
        self.assertEqual(self.babbler.is_enabled('superchat'), True)
        # self.assertNotEqual(self.babbler.is_enabled('gigachat'), True)

    def test_reload(self):
        self.assertEqual(self.babbler.reload(), True)

    def test_talk(self):
        sleep(int(self.babbler.config["babbler_period"]))
        self.assertEqual(self.babbler.talk('superchat', 'трям'), "Здорово!")

    def test_think(self):
        self.assertNotEqual(self.babbler.think('Трям'), "")
        self.assertNotEqual(self.babbler.think('Привет'), "")
        self.assertEqual(self.babbler.think('Кукареку'), "")
"""