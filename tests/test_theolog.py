from unittest import TestCase
import json
import theolog
import test_softice
import softice
from pathlib import Path
from sys import platform

class CTestTheolog(TestCase):

    def setUp(self) -> None:
        
        with open('unittest_config.json', "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY] + theolog.THEOLOG_FOLDER
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY] + theolog.THEOLOG_FOLDER
        self.theolog: theolog.CTheolog = theolog.CTheolog(self.config, self.data_path)
        # self.theolog.reload()


    def test_search_in_book(self):
        
        #def search_in_book(pbook_file: str, pbook_title: str, pphrase: str):
        self.assertIn("и почил в день седьмый", theolog.search_in_book(self.data_path+"1.txt", "Книга Бытия", "И совершил Бог к седьмому дню дела Свои".lower()))
        self.assertNotIn("\n", theolog.search_in_book(self.data_path+"1.txt", "Книга Бытия", "Пусть бегут неуклюже".lower()))
    
