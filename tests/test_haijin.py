from unittest import TestCase
import json
from sys import platform
from pathlib import Path

import softice
import test_softice
import haijin

class CTestHaijin(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]

        self.haijin: haijin.CHaijin = haijin.CHaijin(self.config, self.data_path)


    def test_can_process(self):

        self.assertFalse(self.haijin.can_process("fakechat", "!hk"))
        self.assertFalse(self.haijin.can_process("emptychat", "!хк+"))
        self.assertTrue(self.haijin.can_process(test_softice.TESTPLACE_CHAT_NAME, "!хк"))
        self.assertTrue(self.haijin.can_process(test_softice.TESTPLACE_CHAT_NAME, "!хк+"))
        self.assertTrue(self.haijin.can_process(test_softice.TESTPLACE_CHAT_NAME, "!хк-"))
        self.assertTrue(self.haijin.can_process(test_softice.TESTPLACE_CHAT_NAME, "!hksv"))
        self.assertTrue(self.haijin.can_process(test_softice.TESTPLACE_CHAT_NAME, "!hkrl"))
        self.assertTrue(self.haijin.can_process(test_softice.TESTPLACE_CHAT_NAME, "!hokku"))
        self.assertFalse(self.haijin.can_process(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"))


    def test_get_help(self):

        self.assertIn("хк, hk : получить случайное хокку, \n", self.haijin.get_help(test_softice.TESTPLACE_CHAT_NAME))

""""
    def test_get_hint(self):

        self.assertIn("звонарь, ringer", self.bellringer.get_hint(test_softice.TESTPLACE_CHAT_NAME))

    def test_haijin(self):

        self.assertEqual(self.bellringer.bellringer(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                    "!звать"), "")
        self.assertIn("звонить", self.bellringer.bellringer(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                            "!звонарь"))
        self.assertIn("добавлен", self.bellringer.bellringer(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                            "!игрок+ @test_user"))
        self.assertIn("уже есть", self.bellringer.bellringer(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                            "!игрок+ @test_user"))
        self.assertIn("удален", self.bellringer.bellringer(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                            "!игрок- @test_user"))
        self.assertIn("отсутствует", self.bellringer.bellringer(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                                            "!игрок- @test_user"))
        self.assertIn("поохотимся", self.bellringer.bellringer(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],

    def test_is_enabled(self):

        self.assertFalse(self.bellringer.is_enabled("fakechat"))
        self.assertFalse(self.bellringer.is_enabled("emptychat"))
        self.assertTrue(self.bellringer.is_enabled(test_softice.TESTPLACE_CHAT_NAME))


    def test_is_master(self):

        self.assertFalse(self.bellringer.is_master("user"))
        self.assertTrue(self.bellringer.is_master(self.config["master"]))


    def tearDown(self):

        for file in Path(self.bellringer.data_path).glob("TestPlace.txt*"):

            file.unlink()
"""
