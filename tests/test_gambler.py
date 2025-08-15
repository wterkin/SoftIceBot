from unittest import TestCase
import json
from sys import platform

import softice
import test_softice
import gambler

class CTestGambler(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        self.gambler: gambler.CGambler = gambler.CGambler(self.config)

    """
    def test_gambler(self):

        # def barman(self, pchat_title: str, puser_name: str, puser_title: str,
        #       pmessage_text: str) -> str:
        self.assertNotEqual(self.gambler.gambler(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                               self.config["master_name"], "!пиво"), "")
        self.assertIn(self.config["master_name"], self.gambler.gambler(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                  self.config["master_name"], "!пиво "+self.config["master_name"]))
        self.assertEqual(self.gambler.gambler(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                            self.config["master_name"], "!виски"), "")
        self.assertIn("Сегодня в баре", self.gambler.gambler(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                           self.config["master_name"], "!bar"))
        self.assertEqual(self.gambler.gambler(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                            self.config["master_name"], "!brreload"), "Ассортимент бара обновлён.")
        self.assertIn("У вас нет на это прав", self.gambler.gambler(test_softice.TESTPLACE_CHAT_NAME, "user", "User", "!brreload"))
    """

    def test_can_process(self):

        self.assertFalse(self.gambler.can_process("fakechat", "!спок"))
        self.assertFalse(self.gambler.can_process("emptychat", "!coin"))
        self.assertTrue(self.gambler.can_process(test_softice.TESTPLACE_CHAT_NAME, "!камень"))
        self.assertFalse(self.gambler.can_process(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"))
        self.assertTrue(self.gambler.can_process(test_softice.TESTPLACE_CHAT_NAME,  "!монета"))


    def test_get_help(self):

        self.assertEqual(self.gambler.get_help("fakechat"), "")
        self.assertEqual(self.gambler.get_help("emptychat"), "")
        result = "камень, ножницы, бумага, ящерица, спок\n монета, coin\n"
        self.assertIn(result, self.gambler.get_help(test_softice.TESTPLACE_CHAT_NAME))

    def test_get_hint(self):

        self.assertEqual(self.gambler.get_hint("fakechat"), "")
        self.assertEqual(self.gambler.get_hint("emptychat"), "")
        self.assertIn("игра, game", self.gambler.get_hint(test_softice.TESTPLACE_CHAT_NAME))


    def test_is_enabled(self):


        self.assertFalse(self.gambler.is_enabled("fakechat"))
        self.assertFalse(self.gambler.is_enabled("emptychat"))
        self.assertTrue(self.gambler.is_enabled(test_softice.TESTPLACE_CHAT_NAME))
