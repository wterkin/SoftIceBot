from unittest import TestCase
import json
from sys import platform
from pathlib import Path
import os

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


    def test_format_hokku(self):

      text = "Печальный мир. / Даже когда расцветают вишни.. / Даже тогда..."
      # result_text = 
      result_text = f"{haijin.BOLD}{haijin.ITALIC}{func.screen_text(text)[:-1]}{haijin.ITALIC}{haijin.BOLD}{haijin.LF}" \
                    f"{haijin.AUTHOR_INDENT}{func.screen_text('Исса')} {haijin.SPOILER}" + \
                    f"{haijin.DELIMITER} 1 {haijin.DELIMITER} {len(text)} {haijin.SPOILER}"
      self.assertEqual(haijin.format_hokku(text), result_text)


    def test_get_help(self):

        self.assertIn("хк, hk : получить случайное хокку, \n", self.haijin.get_help(test_softice.TESTPLACE_CHAT_NAME))


    def test_get_hint(self):

        self.assertIn("хокку, hokku", self.haijin.get_hint(test_softice.TESTPLACE_CHAT_NAME))


    def test_get_command(self):

        self.assertEqual(haijin.get_command("hk"), haijin.ASK_HOKKU_CMD)
        self.assertEqual(haijin.get_command("hk+"), haijin.ADD_HOKKU_CMD)
        self.assertEqual(haijin.get_command("hk-"), haijin.DEL_HOKKU_CMD)
      

    def test_haijin(self):

        self.assertEqual(self.haijin.haijin(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                            self.config["master_name"], "!hkrl"), "#Книга загружена")
        self.assertEqual(self.haijin.haijin(test_softice.TESTPLACE_CHAT_NAME, self.config["master"],
                                            self.config["master_name"], "!hksv"), "#Книга сохранена")
        # os.remove(self.haijin.data_path + "hokku.txt_*")
        for file in Path(self.haijin.data_path).glob("hokku.txt_*"):

            file.unlink()
        
        self.assertIn("хк, hk : получить случайное хокку, \n", self.haijin.get_help(test_softice.TESTPLACE_CHAT_NAME))

    def test_is_enabled(self):

        self.assertFalse(self.haijin.is_enabled("fakechat"))
        self.assertFalse(self.haijin.is_enabled("emptychat"))
        self.assertTrue(self.haijin.is_enabled(test_softice.TESTPLACE_CHAT_NAME))


    def test_is_master(self):

        self.assertEqual(self.haijin.is_master("user", "User"), (False, f"У вас нет на это прав, User."))
        self.assertTrue(self.haijin.is_master(self.config["master"], self.config["master_name"]))


    def test_process_command(self):

        #print(f"{self.haijin.hokku=}")
        result = "[1] Печальный мир. / Даже когда расцветают вишни.. / Даже тогда... (Исса)"
        self.assertIn(result, self.haijin.process_command(["hk"], self.config["master"], self.config["master_name"]))
        # Утром / Тихонько упал на землю / С дерева лист. (Кобаяси Исса)
        hokku = "Утром / Тихонько упал на землю / С дерева лист. (Кобаяси Исса)"
        self.assertIn("Спасибо, Петрович, хокку добавлено под номером 2",
                      self.haijin.process_command(["hk+", hokku],
                                                     self.config["master"], self.config["master_name"]))
        self.assertIn("Хокку 2 удалена.", self.haijin.process_command(["hk-", "2"],self.config["master"], self.config["master_name"]))
        # Запрос на удаление от нелегитимного лица
        result = "Извини, User, только Петрович может удалять хокку"
        self.assertIn(result, self.haijin.process_command(["hk-", "1"], "user", "User"))
        
