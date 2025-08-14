from unittest import TestCase
import json
from sys import platform
from pathlib import Path

import softice
import test_softice
import bellringer

class CTestBellRinger(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]

        self.bellringer: bellringer.CBellRinger = bellringer.CBellRinger(self.config, self.data_path)

    def test_bellringer(self):

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
                                                               "!звонить"))

    def test_can_process(self):

        self.assertFalse(self.bellringer.can_process("fakechat", "!звон"))
        self.assertFalse(self.bellringer.can_process("emptychat", "!звонарь"))
        self.assertTrue(self.bellringer.can_process(test_softice.TESTPLACE_CHAT_NAME, "!звон"))
        self.assertFalse(self.bellringer.can_process(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"))


    def test_get_help(self):

        self.assertIn("звонить, звон", self.bellringer.get_help(test_softice.TESTPLACE_CHAT_NAME))


    def test_get_hint(self):

        self.assertIn("звонарь, ringer", self.bellringer.get_hint(test_softice.TESTPLACE_CHAT_NAME))


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
