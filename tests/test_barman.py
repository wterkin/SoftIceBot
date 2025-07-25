from unittest import TestCase
import barman
import json
from sys import platform

import softice
import test_softice

class CTestBarman(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]

        self.barman: barman.CBarman = barman.CBarman(self.config, self.data_path)
        self.barman.reload()


    def test_barman(self):

        # def barman(self, pchat_title: str, puser_name: str, puser_title: str,
        #       pmessage_text: str) -> str:
        self.assertNotEqual(self.barman.barman(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                               self.config["master_name"], "!пиво"), "")
        self.assertIn(self.config["master_name"], self.barman.barman(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                  self.config["master_name"], "!пиво "+self.config["master_name"]))
        self.assertEqual(self.barman.barman(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                            self.config["master_name"], "!виски"), "")
        self.assertIn("Сегодня в баре", self.barman.barman(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                           self.config["master_name"], "!bar"))
        self.assertEqual(self.barman.barman(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                            self.config["master_name"], "!brreload"), "Ассортимент бара обновлён.")
        self.assertIn("У вас нет на это прав", self.barman.barman(test_softice.TESTPLACE_CHAT_NAME, "user", "User", "!brreload"))


    def test_can_process(self):

        self.assertFalse(self.barman.can_process("fakechat", "!пиво"))
        self.assertFalse(self.barman.can_process("emptychat", "!beer"))
        self.assertTrue(self.barman.can_process(test_softice.TESTPLACE_CHAT_NAME, "!beer"))
        self.assertFalse(self.barman.can_process(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"))
        self.assertTrue(self.barman.can_process(test_softice.TESTPLACE_CHAT_NAME,  "!bar"))
        self.assertTrue(self.barman.can_process(test_softice.TESTPLACE_CHAT_NAME,  "!brreload"))


    def test_get_help(self):

        self.assertEqual(self.barman.get_help("fakechat"), "")
        self.assertEqual(self.barman.get_help("emptychat"), "")
        self.assertIn("чай, tea, чй, te", self.barman.get_help(test_softice.TESTPLACE_CHAT_NAME))

    def test_get_hint(self):

        self.assertEqual(self.barman.get_hint("fakechat"), "")
        self.assertEqual(self.barman.get_hint("emptychat"), "")
        self.assertIn("бар, bar", self.barman.get_hint(test_softice.TESTPLACE_CHAT_NAME))


    def test_is_enabled(self):


        self.assertFalse(self.barman.is_enabled("fakechat"))
        self.assertFalse(self.barman.is_enabled("emptychat"))
        self.assertTrue(self.barman.is_enabled(test_softice.TESTPLACE_CHAT_NAME))


    def test_is_master(self):

        self.assertFalse(self.barman.is_master("user"))
        self.assertTrue(self.barman.is_master(self.config["master"]))


    def test_serve_client(self):

        self.assertIn("Балтика", self.barman.serve_client(self.config["master_name"], "пиво"))
        self.assertIn("Балтика", self.barman.serve_client("Юзер", "beer"))
        self.assertEqual(self.barman.serve_client("Юзер", "кузинатра"), "")
