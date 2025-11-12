from unittest import TestCase
import json
from sys import platform
import telebot
import softice
import test_softice
import functions as func
import constants as cn
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

        #  1 # (?:^| )[6бмп]+л+([яR@]+|(9\|)|(еа))*[дт]*[ьъb]*(?!м)(?!ж)        
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex(" млять пофуй"))
        self.assertNotEqual(self.moderator.check_bad_words_ex("вразумляться"), moderator.CENSORED)
        self.assertNotEqual(self.moderator.check_bad_words_ex("римляныня"), moderator.CENSORED)
        self.assertNotEqual(self.moderator.check_bad_words_ex("земля"), moderator.CENSORED)
        self.assertNotEqual(self.moderator.check_bad_words_ex("земляне"), moderator.CENSORED)
        #  2 # \s*[по]*[хxпф][yу][ий(ясе)](?!ть)(?!тыня)
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пофуй"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("фуясе"))
        self.assertNotEqual(self.moderator.check_bad_words_ex("похулить"), moderator.CENSORED)
        self.assertNotEqual(self.moderator.check_bad_words_ex("застрахуй"), moderator.CENSORED)
        #  3 # (?:^| )((н[еe])|(п[оo])|(н[а@])|(н[иu]))*[фxх][еe][рp]((?!ить)|[а@]ч)
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("ферачить"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пофер"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("ниферасе"))
        self.assertNotEqual(self.moderator.check_bad_words_ex("похерить"), moderator.CENSORED)
        self.assertNotEqual(self.moderator.check_bad_words_ex("парикмахерская"), moderator.CENSORED)
        #  4 # \s*п[еeиu][сcз3][дтT][аaиuеe]+(ть)*
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("писта"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пистеть"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("писти"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пистюк"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("nucтюль"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("pa3nucтяй"))
        self.assertNotEqual(self.moderator.check_bad_words_ex("пистон"), moderator.CENSORED)
        #  5 # \s*[пn][иuеe]*[сcзz]+[дтd]+[еёeя]+[цтсcшж]*
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пистеш"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пестеть"))
        #  6 # \s*[йиu]*[уy]*[xхф]
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("йуф"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("uyx"))
        #  7 # \s*[пn][иu][пn][еe]ц
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("пипец"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("nuneц"))
        #  8 # \s*[xхф][уy][яR][кk]
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("фуяк"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("фyяk"))
        #  9 # \s*[жпn][оo0@][пn][ауеaye@]
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("попа"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("nony"))
        # 10 # \s*([нH][аa@])*([з3][аa@])*([пn][рp][оo])*([пn][оo0])[еёeиu][пnб6](ать)*(ал)*а*
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("наипать"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("npounaть"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("3aиnaть"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("проипала"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("поипал"))
        # 11 # \s*(в[ъь])*[еeиu][пnб6](ан)*(ут)*л*
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("въипал"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("unaнутый"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("уиnaн"))
        # 12 # \s*(([сc]ц)|[cс])[уy][кk]+[aа]*[oо0]*
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("сука"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("cцyk0"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("сцук"))
        # 13 # \s*([пn]оo0)*(н[аa@])*[уy]*[сc][рp][аa@]ть([cс]я)*
        self.assertIn(moderator .CENSORED, self.moderator.check_bad_words_ex("наcp@ть"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("п0ср@mь"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("усраться"))
        # 14 # \s*[oо0]*([пn][рp][иu])*[сc]*[фхб][уy][еe]([тm][ьb])*л*
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("обуел"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("прифуеть"))
        self.assertIn(moderator.CENSORED, self.moderator.check_bad_words_ex("cбуeл"))
        self.assertNotIn(moderator.CENSORED, self.moderator.check_bad_words_ex("ибо"))
        self.assertNotIn(moderator.CENSORED, self.moderator.check_bad_words_ex("enjoy"))
        self.assertNotIn(moderator.CENSORED, self.moderator.check_bad_words_ex("благодарю"))
        self.assertNotIn(moderator.CENSORED, self.moderator.check_bad_words_ex("плохо"))
        # попался
        
    def test_control_talking(self):
        
        record: dict = {}
        record[cn.MCONTENT_TYPE] = "text"
        record[cn.MTEXT] = "мля"
        record[cn.MCAPTION] = "мля"
        record[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        record[cn.MCHAT_ID] = test_softice.TESTPLACE_CHAT_ID
        record[cn.MMESSAGE_ID] = 0
        record[cn.MUSER_TITLE] = self.config["master_name"]
        record[cn.MUSER_LASTNAME] = ""
        self.assertIn(moderator.CENSORED, self.moderator.control_talking(record))
        record[cn.MTEXT] = "абырвалг"
        self.assertEqual(self.moderator.control_talking(record), "")
        # *** Если сообщение пустое - не обрабатывается
        record[cn.MTEXT] = ""
        self.assertEqual(self.moderator.control_talking(record), "")
        # *** Проверка разрешенных чатов
        record[cn.MCHAT_TITLE] = "fakechat"
        record[cn.MTEXT] = "мля"
        self.assertEqual(self.moderator.control_talking(record), "")
        record[cn.MCHAT_TITLE] = "emptychat"
        self.assertEqual(self.moderator.control_talking(record), "")

        
    def test_get_hint(self):

        self.assertIn(", ".join(moderator.HINT), self.moderator.get_hint(test_softice.TESTPLACE_CHAT_NAME))


    def test_is_enabled(self):

        self.assertFalse(self.moderator.is_enabled("fakechat"))
        self.assertFalse(self.moderator.is_enabled("emptychat"))
        self.assertTrue(self.moderator.is_enabled(test_softice.TESTPLACE_CHAT_NAME))


    def test_is_master(self):

        self.assertEqual(self.moderator.is_master("user", "User"), (False, f"У вас нет на это прав, User."))
        self.assertTrue(self.moderator.is_master(self.config["master"], self.config["master_name"]))

    
    def test_moderator(self): 
        
        record: dict = {}
        record[cn.MCONTENT_TYPE] = "text"
        record[cn.MTEXT] = "абырвалг"
        record[cn.MCHAT_TITLE] = test_softice.TESTPLACE_CHAT_NAME
        record[cn.MCHAT_ID] = test_softice.TESTPLACE_CHAT_ID
        record[cn.MMESSAGE_ID] = 0
        record[cn.MUSER_NAME] = self.config["master"]
        record[cn.MUSER_TITLE] = self.config["master_name"]
        record[cn.MUSER_LASTNAME] = ""
        self.assertEqual(self.moderator.moderator(record), "")
        record[cn.MTEXT] = "!bwrl"
        self.assertIn("Словарь", self.moderator.moderator(record))
        record[cn.MUSER_NAME] = "user"
        record[cn.MUSER_TITLE] = "User"
        self.assertIn("Извини", self.moderator.moderator(record))
        record[cn.MCHAT_TITLE] = "fakechat"
        record[cn.MTEXT] = "!bwrl"
        self.assertEqual(self.moderator.control_talking(record), "")
        record[cn.MCHAT_TITLE] = "emptychat"
        self.assertEqual(self.moderator.control_talking(record), "")
