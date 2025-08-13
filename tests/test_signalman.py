from unittest import TestCase
import json
from sys import platform
import database as db
import softice
import test_softice
import signalman

class CTestSignalman(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]

        self.database: db.CDataBase = db.CDataBase(self.config, self.data_path)
        if not self.database.exists():

            # *** А нету ещё БД, создавать нужно.
            self.database.create()

        self.signalman: signalman.CSignalMan = signalman.CSignalMan(self.config, self.database)


    def test_can_process(self):

        self.assertFalse(self.signalman.can_process("fakechat", "!monitor"))
        self.assertFalse(self.signalman.can_process("emptychat", "!мон"))
        self.assertTrue(self.signalman.can_process(test_softice.TESTPLACE_CHAT_NAME, "!mon"))
        self.assertFalse(self.signalman.can_process(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"))
        self.assertTrue(self.signalman.can_process(test_softice.TESTPLACE_CHAT_NAME,  "!signal"))
        self.assertTrue(self.signalman.can_process(test_softice.TESTPLACE_CHAT_NAME,  "!монитор"))

    def test_get_help(self):

        self.assertEqual(self.signalman.get_help("fakechat"), "")
        self.assertEqual(self.signalman.get_help("emptychat"), "")
        self.assertIn(", ".join(signalman.COMMANDS), self.signalman.get_help(test_softice.TESTPLACE_CHAT_NAME))

    def test_get_hint(self):

        self.assertEqual(self.signalman.get_hint("fakechat"), "")
        self.assertEqual(self.signalman.get_hint("emptychat"), "")
        self.assertIn("сигнал, signal", self.signalman.get_hint(test_softice.TESTPLACE_CHAT_NAME))

