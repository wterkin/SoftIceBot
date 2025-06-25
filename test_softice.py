from unittest import TestCase
import softice


class CTestSoftIceBot(TestCase):

    def setUp(self) -> None:

        print("-"*40)
        print("* Creating bot instance")
        self.bot = softice.CSoftIceBot()
        # print("* Loading demo config")
        # self.bot.load_config("unittest_config.json")

    def test_is_foreign_command(self):

        # TrueMafiaBot
        print("+ test_is_foreign_command:TrueMafiaBot, ok")
        self.assertEqual(self.is_foreign_command ("TrueMafiaBot"), True)
        print("+ test_is_foreign_command:SuperPuperBot, ok")
        self.assertEqual(self.is_foreign_command ("SuperPuperBot"), True)

    def test_is_master(self):
        print("+ test_is_master:username, ok")
        self.assertEqual(self.bot.is_master('username'), True)
        print("+ test_is_master:User, wrong")
        self.assertNotEqual(self.bot.is_master('User'), True)

    def test_is_this_chat_enabled(self):
        print("+ test_is_this_chat_enabled:superchat, ok")
        self.assertEqual(self.bot.is_this_chat_enabled('superchat'), True)
        print("+ test_is_this_chat_enabled:supermegachat, wrong")
        self.assertEqual(self.bot.is_this_chat_enabled('supermegachat'), False)

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
