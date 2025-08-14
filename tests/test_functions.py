from unittest import TestCase
import functions as func
import json
# from sys import platform
from pathlib import Path

from sys import platform
import softice
import test_softice

class CTestFunctions(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]


    def test_parse_input(self):

        self.assertEqual(func.parse_input("!test softice"), ["test", "softice"])


    def test_get_command(self):

        self.assertEqual(func.get_command("test",["run", "test", "stop"]), 1)


    def test_load_from_file(self):

        lines: list = ["line1", "line2", "line3"]
        file_name: str = self.data_path+"test_function.txt"
        func.save_list(lines, file_name)
        self.assertEqual(func.load_from_file(file_name), ["line1", "line2", "line3"])
        self.assertEqual(func.load_from_file(self.data_path+"ABCDEF"), [])
        for file in Path(self.data_path).glob(file_name):

            file.unlink()
