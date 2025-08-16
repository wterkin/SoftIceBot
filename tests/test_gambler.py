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


    def test_can_process(self):

        self.assertFalse(self.gambler.can_process("fakechat", "!спок"))
        self.assertFalse(self.gambler.can_process("emptychat", "!coin"))
        self.assertTrue(self.gambler.can_process(test_softice.TESTPLACE_CHAT_NAME, "!камень"))
        self.assertFalse(self.gambler.can_process(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"))
        self.assertTrue(self.gambler.can_process(test_softice.TESTPLACE_CHAT_NAME,  "!монета"))


    def test_get_help(self):

        self.assertEqual(self.gambler.get_help("fakechat"), "")
        self.assertEqual(self.gambler.get_help("emptychat"), "")
        self.assertIn("камень", self.gambler.get_help(test_softice.TESTPLACE_CHAT_NAME))
        self.assertIn("спок", self.gambler.get_help(test_softice.TESTPLACE_CHAT_NAME))
        self.assertIn("монета", self.gambler.get_help(test_softice.TESTPLACE_CHAT_NAME), )
        

    def test_get_hint(self):

        self.assertEqual(self.gambler.get_hint("fakechat"), "")
        self.assertEqual(self.gambler.get_hint("emptychat"), "")
        self.assertIn("игра, game", self.gambler.get_hint(test_softice.TESTPLACE_CHAT_NAME))


    def test_is_enabled(self):


        self.assertFalse(self.gambler.is_enabled("fakechat"))
        self.assertFalse(self.gambler.is_enabled("emptychat"))
        self.assertTrue(self.gambler.is_enabled(test_softice.TESTPLACE_CHAT_NAME))
