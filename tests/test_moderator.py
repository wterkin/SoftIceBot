from unittest import TestCase
import json
from sys import platform
import telebot
import softice
import test_softice
import functions as func
import moderator

class CTestModerator(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[softice.LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[softice.WINDOWS_DATA_FOLDER_KEY]
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[softice.TOKEN_KEY])
        self.moderator: moderator.CModerator = moderator.CModerator(self.robot, self.config, self.data_path)

    def test_replace_bad_words(self):
        
        self.assertEqual(moderator.replace_bad_words("чатлане","Жадный, как все чатлане"), 
                         f"Жадный, как все {moderator.CENSORED}")

    def test_can_process(self):

        self.assertFalse(self.moderator.can_process("fakechat", "!adm"))
        self.assertFalse(self.moderator.can_process("emptychat", "!adm"))
        self.assertTrue(self.moderator.can_process(test_softice.TESTPLACE_CHAT_NAME, "!adm"))
        self.assertTrue(self.moderator.can_process(test_softice.TESTPLACE_CHAT_NAME, "!bwrl"))
        self.assertFalse(self.moderator.can_process(test_softice.TESTPLACE_CHAT_NAME, "!кукабарра"))

    
    def test_check_bad_words_ex(self):
    
        #def check_bad_words_ex(self, pmessage: str) -> str:
        self.assertEqual(self.moderator.check_bad_words_ex(""), "")
        # .*\s*[6бмп]+л+[яR@]+(9|)*[дт]*[ьъb]*(?!м)(?!ж)
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex(" млять пофуй"))
        self.assertNotEqual(self.moderator.check_bad_words_ex("Вразумляться"), moderator.CENSORED)
        self.assertNotEqual(self.moderator.check_bad_words_ex("Римляныня"), moderator.CENSORED)
        # \s*[по]*[хxпф][yу][ий(ясе)](?!ть)(?!тыня)
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пофуй"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("фуясе"))
        self.assertNotEqual(self.moderator.check_bad_words_ex("похулить"), moderator.CENSORED)
        # .*\s*[xх]е[рp][а@]*(?!ить)\s*
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("ферачить"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пофер"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("ниферасе"))
        self.assertNotEqual(self.moderator.check_bad_words_ex("похерить"), moderator.CENSORED)

        # парикмахерская
    def test_get_hint(self):

        self.assertIn(", ".join(moderator.HINT), self.moderator.get_hint(test_softice.TESTPLACE_CHAT_NAME))
