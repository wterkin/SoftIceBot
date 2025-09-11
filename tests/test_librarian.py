from unittest import TestCase
import json
import librarian
import test_softice


class CTestLibrarian(TestCase):

    def setUp(self) -> None:
        with open('unittest_config.json', "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config, self.config["windows_data_folder"])
        self.librarian.reload()

    def test_find_in_book(self):
        
        book: list = ["Не экономь на душе. Не наготовить запасов там, где должно трудиться сердце. Отдать - значит перебросить мост через бездну своего одиночества. Антуан де Сент-Экзюпери",
                      "Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри..."]
        word_list: list = "Мы думаем".split(" ")
        self.assertEqual(librarian.find_in_book(book, word_list), "[2]"+book[1])
        
        
    def test_get_command(self):
        
        self.assertEqual(librarian.get_command("qt"), librarian.ASK_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt?"), librarian.FIND_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt+"), librarian.ADD_QUOTE_CMD)
        self.assertEqual(librarian.get_command("qt-"), librarian.DEL_QUOTE_CMD)


    def test_quote(self):
        
        self.assertEqual(librarian.quote(["No fate.",], [""],), "[1] No fate.")
        self.assertEqual(librarian.quote(["No fate.",], ["qt", "0"],), "Номер должен быть больше нуля")
        self.assertEqual(librarian.quote(["No fate.",], ["qt", "5"],), "Номер должен быть от 1 до 1")
        self.assertEqual(librarian.quote(["No fate.",], ["fate"],), "[1] No fate.")
        self.assertEqual(librarian.quote(["No fate.",], ["1"],), "[1] No fate.")
        
    
    def test_can_process(self):
        
        self.assertEqual(self.librarian.can_process(test_softice.TESTPLACE_CHAT_NAME, '!цт'), True)
        self.assertEqual(self.librarian.can_process('fakechat', '!цт'), False)
        self.assertEqual(self.librarian.can_process('empttychat', '!хквс'), False)


    def test_execute_quotes_commands(self):

        result = "Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри..."
        self.assertIn(result, self.librarian.execute_quotes_commands(self.config["master"], self.config["master_name"],
                                                                     [""], librarian.ASK_QUOTE_CMD))

        quote = "Нет у тебя, человек, ничего, кроме души. Пифагор"
        self.assertIn("Спасибо, Петрович, цитата добавлена под номером 2",
                      self.librarian.execute_quotes_commands(self.config["master"], self.config["master_name"],
                                                     ["qt+", quote], librarian.ADD_QUOTE_CMD))
        self.assertIn("Цитата 2 удалена", 
                      self.librarian.execute_quotes_commands(self.config["master"], self.config["master_name"],
                      ["hk-", "2"], librarian.DEL_QUOTE_CMD))
        # Запрос на удаление от нелегитимного лица
        result = "Извини, User, только Петрович может удалять цитаты"
        self.assertIn(result, self.librarian.execute_quotes_commands("user", "User", ["hk-", "1"], librarian.DEL_QUOTE_CMD))


    def test_get_help(self):
        
        self.assertNotEqual(self.librarian.get_help(test_softice.TESTPLACE_CHAT_NAME), "")
        self.assertEqual(self.librarian.get_help("fakechat"), "")
        self.assertEqual(self.librarian.get_help("emptychat"), "")


    def test_get_hint(self):
        
        self.assertNotEqual(self.librarian.get_hint(test_softice.TESTPLACE_CHAT_NAME), "")
        self.assertEqual(self.librarian.get_hint("fakechat"), "")
        self.assertEqual(self.librarian.get_hint("emptychat"), "")


    def test_is_enabled(self):
        
        self.assertTrue(self.librarian.is_enabled(test_softice.TESTPLACE_CHAT_NAME))
        self.assertFalse(self.librarian.is_enabled("fakechat"))
        self.assertFalse(self.librarian.is_enabled("emptychat"))


    def test_is_master(self):
        
        self.assertTrue(self.librarian.is_master(self.config["master"], self.config["master_name"]))
        self.assertEqual(self.librarian.is_master('User', 'Юзер'), (False, 'У вас нет на это прав, Юзер.'))
       

    def test_librarian(self):

        self.assertEqual(self.librarian.librarian('fakechat', 'User', 'Юзер', '!lbreload'), "")
        self.assertEqual(self.librarian.librarian('emptychat', 'User', 'Юзер', '!lbreload'), "")
        self.assertEqual(self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME, 
                                                  self.config["master"], self.config["master_name"], '!lbreload'),
                                                  "Книга обновлена") 
        self.assertEqual(self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME, 'User', 'Юзер', 
                                                  '!lbreload'), "Извини, Юзер, только Петрович может перегружать цитаты!")
        self.assertEqual(self.librarian.librarian('fakechat', 'User', 'Юзер', '!lbsave'), "")
        self.assertEqual(self.librarian.librarian('emptychat', 'User', 'Юзер', '!lbsave'), "")
        self.assertEqual(self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME, 
                                                  self.config["master"], self.config["master_name"], "!lbsave"),
                                                  "Книга сохранена") 
        self.assertEqual(self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME, "User", "Юзер", 
                                                  '!lbsave'), "Извини, Юзер, только Петрович может сохранять цитаты!")
        self.assertIn("quoteadd", self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME, 'user', 'Юзер', '!библиотека'))
        self.assertEqual(self.librarian.librarian("fakechat", 'user', 'Юзер', '!библиотека'), "")
        self.assertEqual(self.librarian.librarian("emptychat", 'user', 'Юзер', '!библиотека'), "")
        self.assertIn("Спасибо, Петрович, цитата добавлена под номером 2",
                      self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME, 
                                               self.config["master"], self.config["master_name"], "!qt+ No fate"))
        self.assertIn("Цитата 2 удалена", 
                      self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME,
                                               self.config["master"], self.config["master_name"], "!qt- 2"))

        self.assertEqual(self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME, "user", "Юзер", "!qt- 2"),
                                                  "Извини, Юзер, только Петрович может удалять цитаты")     
        self.assertEqual(self.librarian.librarian(test_softice.TESTPLACE_CHAT_NAME, "user", "Юзер", "!qt"), 
                                             "[1] Мы думаем, что Бог видит нас сверху - но Он видит нас изнутри...")
