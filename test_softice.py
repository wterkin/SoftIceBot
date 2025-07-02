from unittest import TestCase
import softice
import constants as cn
from datetime import datetime, timedelta

class CTestSoftIceBot(TestCase):


    def setUp(self) -> None:

        print("-"*40)
        print("* Creating bot instance")
        self.bot = softice.CSoftIceBot()


    def test_is_foreign_command(self):

        # TrueMafiaBot
        print("+ test_is_foreign_command:TrueMafiaBot")
        self.assertEqual(softice.is_foreign_command ("TrueMafiaBot"), True)
        print("+ test_is_foreign_command:SuperPuperBot")
        self.assertNotEqual(softice.is_foreign_command ("SuperPuperBot"), True)


    def test_is_chat_legitimate(self):
        print("+ test_is_chat_legitimate:TestPlace")
        self.bot.event[cn.MCHAT_TITLE] = 'TestPlace'
        self.bot.event[cn.MCHAT_ID] = -1002089030820
        self.assertEqual(self.bot.is_chat_legitimate(), "")
        print("+ test_is_chat_legitimate:megachat")
        self.bot.event[cn.MCHAT_TITLE] = 'megachat'
        self.bot.event[cn.MCHAT_ID] = -1002287597239
        self.assertEqual(self.bot.is_chat_legitimate(), softice.NON_LEGITIMATE_CHAT_MSG)
        print("+ test_is_chat_legitimate:private")
        self.bot.event[cn.MCHAT_TITLE] = None
        self.assertEqual(self.bot.is_chat_legitimate(), softice.PRIVATE_IS_DISABLED_MSG)


    def test_is_master(self):
        print("+ test_is_master:username")
        self.bot.event[cn.MUSER_NAME] = 'username'
        self.assertEqual(self.bot.is_master(), True)
        print("+ test_is_master:User")
        self.bot.event[cn.MUSER_NAME] = 'User'
        self.assertNotEqual(self.bot.is_master(), True)


    def test_is_message_actual(self):
        print("+ test_message_actual")
        self.bot.event[cn.MDATE] = (datetime.now() - timedelta(seconds=30)).timestamp()
        self.assertEqual(self.bot.is_message_actual(), True)
        print("+ test_message_actual")
        self.bot.event[cn.MDATE] = (datetime.now() - timedelta(seconds=120)).timestamp()
        self.assertNotEqual(self.bot.is_message_actual(), True)



"""
    def test_process_command(self):
        print("+ test_process_command:user ok, config")
        self.assertEqual(self.bot.process_command("config", -583831606, "superchat",
                                                  {"name": "username", "title": "usertitle"}), True)
        print("+ test_process_command:user wrong, config")
        self.assertEqual(self.bot.process_command("config", -583831606, "superchat",
                                                  {"name": "MegaUser", "title": "Юзер"}), False)
        print("+ test_process_command:user ok, help")
        self.assertEqual(self.bot.process_command("help", -583831606, "superchat",
                                                  {"name": "username", "title": "usertitle"}), True)
        print("+ test_process_command:user wrong, unknown command")
        self.assertNotEqual(self.bot.process_command("вон!", -583831606, "superchat",
                                                     {"name": "username", "title": "usertitle"}), True)

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