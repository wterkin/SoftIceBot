from unittest import TestCase
import json
from sys import platform

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

        #  def bellringer(self, pchat_title: str, puser_name: str, pmessage_text: str):
        self.assertEqual(self.bellringer.bellringer(test_softice.TESTPLACE_CHAT_NAME, self.config["master"], "!звать"), "")
        
