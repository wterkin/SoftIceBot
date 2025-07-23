from unittest import TestCase
import barman
import json


class CTestBarman(TestCase):
    def setUp(self) -> None:
        with open('config.sample.json', "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        self.barman: barman.CBarman = barman.CBarman(self.config, self.config["windows_data_folder"])
        self.barman.reload()

    def test_barman(self):
        # def barman(self, pchat_title: str, puser_name: str, puser_title: str,
        #            pmessage_text: str) -> str:
        self.assertNotEqual(self.barman.barman('superchat', 'user', 'Юзер', '!пиво'), '')
        self.assertNotEqual(self.barman.barman('megachat', 'user', 'Юзер', '!beer'), '')
        self.assertEqual(self.barman.barman('gigachat', 'user', 'Юзер', '!beer'), '')

        self.assertNotEqual(self.barman.barman('superchat', 'user', 'Юзер', '!бар'), '')
        self.assertNotEqual(self.barman.barman('megachat', 'user', 'Юзер', '!bar'), '')
        self.assertEqual(self.barman.barman('gigachat', 'user', 'Юзер', '!bar'), '')

        self.assertEqual(self.barman.barman('superchat', 'username', 'usertitle', '!brreload'),
                         "Ассортимент бара обновлён.")
        self.assertEqual(self.barman.barman('megachat', 'username', 'usertitle', '!brreload'),
                         "Ассортимент бара обновлён.")
        self.assertNotEqual(self.barman.barman('gigachat', 'username', 'usertitle', '!brrl'),
                            "Ассортимент бара обновлён.")

        self.assertEqual(self.barman.barman('gigachat', 'user', 'Юзер', '!кукабарра'), "")
        self.assertEqual(self.barman.barman('megachat', 'user', 'Юзер', '!кузинатра'), "")
        self.assertEqual(self.barman.barman('мяучат', 'user', 'Юзер', '!пиво'), "")
        self.assertEqual(self.barman.barman('кукучат', 'user', 'Юзер', '!beer'), "")

    def test_can_process(self):
        self.assertEqual(self.barman.can_process('superchat', '!beer'), True)
        self.assertEqual(self.barman.can_process('megachat', '!пиво'), True)
        self.assertEqual(self.barman.can_process('gigachat', '!кукабарра'), False)

    def test_get_help(self):
        self.assertNotEqual(self.barman.get_help('superchat'), "")
        self.assertNotEqual(self.barman.get_help('megachat'), "")
        self.assertEqual(self.barman.get_help('левочат'), "")

    def test_get_hint(self):
        self.assertNotEqual(self.barman.get_hint('superchat'), "")
        self.assertNotEqual(self.barman.get_hint('megachat'), "")
        self.assertEqual(self.barman.get_hint('левочат'), "")

    def test_is_enabled(self):
        self.assertEqual(self.barman.is_enabled('superchat'), True)
        self.assertEqual(self.barman.is_enabled('megachat'), True)
        self.assertEqual(self.barman.is_enabled('левочат'), False)

    def test_is_master(self):
        self.assertEqual(self.barman.is_master('username'), True)
        self.assertNotEqual(self.barman.is_master('User'), True)

    def test_serve_client(self):
        self.assertNotEqual(self.barman.serve_client('Юзер', 'пиво'), "")
        self.assertNotEqual(self.barman.serve_client('Юзер', 'beer'), "")
        self.assertEqual(self.barman.serve_client('Юзер', 'кузинатра'), "")
