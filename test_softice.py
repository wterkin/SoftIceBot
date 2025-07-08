from unittest import TestCase
import softice
import constants as cn
from datetime import datetime, timedelta
from telebot import types as bt
import debug as dbg

TESTPLACE_CHAT_ID: int = -1002287597239
TESTPLACE_CHAT_NAME : str = 'TestPlace'
BOTOVKA_CHAT_ID: int = -1002089030820


class CTestSoftIceBot(TestCase):


    def setUp(self) -> None:

        print("-"*40)
        print("* Creating bot instance")
        self.bot = softice.CSoftIceBot()


    def test_decode_message(self):

        dbg.dout("***** test_decode_message")
        chat: bt.ChatFullInfo = bt.ChatFullInfo(TESTPLACE_CHAT_ID, type="group")
        user: bt.User = bt.User(self.bot.config["master_id"], False, self.bot.config["master_name"])
        message: bt.Message = bt.Message(1, user,
                                         datetime.now(), chat,
                                         "text", {}, "")
        # *** Text
        message.text = "привет"
        self.bot.decode_message(message)
        self.assertEqual(self.bot.msg_rec[cn.MTEXT], "привет")
        message.text = ""
        self.bot.decode_message(message)
        self.assertEqual(self.bot.msg_rec[cn.MTEXT], "привет")

        # *** Caption
        message.caption = "картинка"
        self.bot.decode_message(message)
        self.assertEqual(self.bot.msg_rec[cn.MCAPTION], "картинка")
        message.caption = ""

        # *** Chat ID
        self.assertEqual(self.bot.msg_rec[cn.MCHAT_ID], TESTPLACE_CHAT_ID)

        # *** Chat Title
        message.chat.title = TESTPLACE_CHAT_NAME
        self.bot.decode_message(message)
        self.assertEqual(self.bot.msg_rec[cn.MCHAT_TITLE], TESTPLACE_CHAT_NAME)
        message.chat.title = ""

        # *** User ID
        message.from_user.id = self.bot.config["master_id"]
        self.bot.decode_message(message)
        self.assertEqual(self.bot.msg_rec[cn.MUSER_ID], self.bot.config["master_id"])
        message.from_user.id = None

        # *** User Name
        message.from_user.username = self.bot.config["master"]
        self.bot.decode_message(message)
        self.assertEqual(self.bot.msg_rec[cn.MUSER_NAME], self.bot.config["master"])
        message.from_user.username = ""


    def test_is_chat_legitimate(self):

        dbg.dout("***** test_is_chat_legitimate")
        # *** TestPlace
        self.bot.event[cn.MCHAT_TITLE] = 'TestPlace'
        self.bot.event[cn.MCHAT_ID] = TESTPLACE_CHAT_ID
        self.assertEqual(self.bot.is_chat_legitimate(), "")
        # *** Fake chat megachat
        self.bot.event[cn.MCHAT_TITLE] = 'megachat'
        self.bot.event[cn.MCHAT_ID] = TESTPLACE_CHAT_ID
        self.assertEqual(self.bot.is_chat_legitimate(), softice.NON_LEGITIMATE_CHAT_MSG)
        # *** Private
        self.bot.event[cn.MCHAT_TITLE] = None
        self.assertEqual(self.bot.is_chat_legitimate(), softice.PRIVATE_IS_DISABLED_MSG)


    def test_is_foreign_command(self):

        dbg.dout("***** test_is_foreign_command")
        # *** Пробуем бота Mafioso
        self.assertEqual(self.bot.is_foreign_command ("Mafioso"), True)
        # *** Пробуем бота SuperPuperBot
        self.assertNotEqual(self.bot.is_foreign_command ("SuperPuperBot"), True)


    def test_is_master(self):

        dbg.dout("***** test_is_master")
        # *** Try master name
        self.bot.event[cn.MUSER_NAME] = self.bot.config["master"]
        self.assertTrue(self.bot.is_master())
        # *** Fake user User
        self.bot.event[cn.MUSER_NAME] = 'User'
        self.assertFalse(self.bot.is_master())


    def test_is_message_actual(self):

        dbg.dout("***** test_is_message_actual")
        # *** Actual message
        self.bot.event[cn.MDATE] = (datetime.now() - timedelta(seconds=30)).timestamp()
        self.assertTrue (self.bot.is_message_actual())
        # *** Outdated message
        self.bot.event[cn.MDATE] = (datetime.now() - timedelta(seconds=61)).timestamp()
        self.assertFalse(self.bot.is_message_actual())


    def test_load_config(self):

        dbg.dout("***** test_load_config")
        self.assertTrue(self.bot.load_config(softice.UNITTEST_CONFIG_NAME))
        self.assertFalse(self.bot.load_config("unittest_bad_config.json"))


    def test_process_command(self):

        # *** Перезагрузка конфига
        self.bot.event[cn.MUSER_NAME] = self.bot.config["master"]
        self.bot.event[cn.MUSER_TITLE] = self.bot.config["master_name"]
        self.bot.event[cn.MCOMMAND] = "config"
        self.assertTrue(self.bot.process_command())
        self.bot.event[cn.MUSER_NAME] = "User"
        self.bot.event[cn.MUSER_TITLE] = "User"
        self.assertFalse(self.bot.process_command())
        # *** Выход
        # EXIT_COMMANDS
        self.bot.event[cn.MUSER_NAME] = self.bot.config["master"]
        self.bot.event[cn.MUSER_TITLE] = self.bot.config["master_name"]
        self.bot.event[cn.MCOMMAND] = "носок"
        self.assertRaises(softice.CQuitByDemand, self.bot.process_command)
        # self.assertEqual(self.bot.process_command(), False)
        # self.assertEqual(self.bot.process_command(), True)
        # self.assertNotEqual(self.bot.process_command(), True)


"""

#    def test_process_modules(self):
#        self.bot.message_text = "!Экспекто патронум"
#        print("+ test_process_modules:??")
#        self.assertEqual(self.bot.process_modules(-583831606, "Ботовка", "Pet_Rovich", "Петрович"),
#                         ("", False))

    def test_reload_config(self):
        # pchat_id: int, puser_name: str, puser_title: str
        print("+ test_reload_config:user ok")
        self.assertEqual(self.bot.reload_config(-583831606, "username", "usertitle"), True)
        print("+ test_reload_config:user wrong")
        self.assertEqual(self.bot.reload_config(-583831606, "user", "user"), False)
"""