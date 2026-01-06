from unittest import TestCase
import json
import theolog
import test_softice
import softice
from pathlib import Path
from sys import platform

class CTestTheolog(TestCase):

    def setUp(self) -> None:
        
        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]
        self.theolog: theolog.CTheolog = theolog.CTheolog(self.config, self.data_path)
        # self.theolog.reload()


    def test_search_in_book(self):
        
        #def search_in_book(pbook_file: str, pbook_title: str, pphrase: str):
        self.assertIn("и почил в день седьмый", theolog.search_in_book(self.data_path+theolog.THEOLOG_FOLDER+"1.txt", "Книга Бытия", "И совершил Бог к седьмому дню дела Свои".lower()))
        self.assertNotIn("\n", theolog.search_in_book(self.data_path+theolog.THEOLOG_FOLDER+"1.txt", "Книга Бытия", "Пусть бегут неуклюже".lower()))
    
    def test_can_process(self):
        
        # def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        self.assertTrue(self.theolog.can_process(test_softice.TESTPLACE_CHAT_NAME, "!bible"))
        self.assertTrue(self.theolog.can_process(test_softice.TESTPLACE_CHAT_NAME, "!книги"))
        self.assertTrue(self.theolog.can_process(test_softice.TESTPLACE_CHAT_NAME, "!найтивз"))
        self.assertFalse(self.theolog.can_process("fakechat", "!bible"))
        self.assertFalse(self.theolog.can_process("empttychat", "!быт 1 1"))


    def test_find_in_book(self):
        
        # def find_in_book(self, pbook_idx: int, pbook_name: str, pchapter: str, pverse: str,
                     # poutput_count: int) -> str:  # noqa
        # print(f"!!!!!!!! {self.data_path=}")
        self.assertIn("небо и землю", self.theolog.find_in_book(0, "Бытие", "1", "", 1))
        self.assertIn("и тьма над бездною", self.theolog.find_in_book(0, "Бытие", "1", "2", 1))
        self.assertEqual(self.theolog.find_in_book(0, "Бытие", "1", "211", 1), "")
        self.assertIn("И был вечер, и было утро", self.theolog.find_in_book(0, "Бытие", "1", "12", 2))

    def test_get_help(self):
        
        # def get_help(self, pchat_title: str) -> str:
        self.assertIn("книги, books", self.theolog.get_help(test_softice.TESTPLACE_CHAT_NAME))
        self.assertIsNone(self.theolog.get_help("fakechat"))
        self.assertIsNone(self.theolog.get_help("emptychat"))        

    def test_get_books(self):
        
        # def get_help(self, pchat_title: str) -> str:
        self.assertIn("Бытие", self.theolog.get_books(test_softice.TESTPLACE_CHAT_NAME))
        self.assertIn("", self.theolog.get_books("fakechat"))
        self.assertIn("", self.theolog.get_books("emptychat"))        


    def test_get_hint(self):
        
        # def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        self.assertIn("библия, bible", self.theolog.get_hint(test_softice.TESTPLACE_CHAT_NAME))
        self.assertIn("", self.theolog.get_hint("fakechat"))
        self.assertIn("", self.theolog.get_hint("emptychat"))        


    def test_global_search(self):
        
        # def global_search(self, ptestament: str, pphrase: str,
                          # pfull_output: bool = False, poutput_count: int = 0) -> str:  # noqa
