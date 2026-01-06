# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль цитатника Библии."""

import re
import random

# from setuptools._distutils.extension import read_setup_file

import functions as func
import prototype

# *** Путь к файлам Библии
THEOLOG_FOLDER: str = "theolog/"
# *** Константы частей сообщения
COMMAND_ARG: int = 0
LINE_ARG: int = 1

# *** Список книг Библии
BIBLE_BOOKS: list = [["бытие", "быт", "Книга Бытия"],
                     ["исход", "исх", "Книга Исход"],
                     ["левит", "лев", "Книга Левит"],
                     ["числа", "числ", "Книга Числа"],
                     ["второзаконие", "втор", "Книга Второзаконие"],
                     ["инавин", "нав", "Книга Иисуса Навина"],
                     ["судей", "суд", " Книга Судей"],
                     ["руфь", "руфь", "Книга Руфи"],
                     ["1царств", "1цар", "1-я книга Царств"],
                     ["2царств", "2цар", "2-я книга Царств"],
                     ["3царств", "3цар", "3-я книга Царств"],
                     ["4царств", "4цар", "4-я книга Царств"],
                     ["1паралипоменон", "1пар", "1-я книга Паралипоменон"],
                     ["2паралипоменон", "2пар", "2-я книга Паралипоменон"],
                     ["ездра", "езд", "Книга Ездры"],
                     ["неемия", "неем", "Книга Неемии"],
                     ["есфирь", "есф", "Книга Есфири"],
                     ["иов", "иов", "Книга Иова"],
                     ["псалтирь", "пс", "Псалтирь"],
                     ["притчи", "притч", "Книга Притчей"],
                     ["екклесиаст", "еккл", "Книга Екклесиаста"],
                     ["песни", "песн", "Песнь Песней"],
                     ["исаии", "ис", "Книга пророка Исайи"],
                     ["иеремии", "иер", "Книга пророка Иеремии"],
                     ["плачиеремии", "плач", "Плач Иеремии"],
                     ["иезекииль", "иез", "Книга пророка Иезекииля"],
                     ["даниил", "дан", "Книга пророка Даниила"],
                     ["осия", "ос", "Книга пророка Осии"],
                     ["иоиль", "иоиль", "Книга пророка Иоиля"],
                     ["амос", "ам", "Книга пророка Амоса"],
                     ["авдий", "ав", "Книга пророка Авдия"],
                     ["иона", "иона", "Книга пророка Ионы"],
                     ["михей", "мих", "Книга пророка Михея"],
                     ["наум", "наум", "Книга пророка Наума"],
                     ["аввакум", "авв", "Книга пророка Аввакума"],
                     ["софония", "соф", "Книга пророка Софонии"],
                     ["аггей", "агг", "Книга пророка Аггея"],
                     ["захария", "зах", "Книга пророка Захарии"],
                     ["малахия", "мал", "Книга пророка Малахии"],
                     ["матфей", "мф", "Евангелие от Матфея"],
                     ["марка", "мк", "Евангелие от Марка"],
                     ["луки", "лк", "Евангелие от Луки"],
                     ["иоанна", "ин", "Евангелие от Иоанна"],
                     ["деяния", "деян", "Деяния апостолов"],
                     ["иакова", "иак", "Послание Иакова"],
                     ["1петра", "1пет", "1-е послание Петра"],
                     ["2петра", "2пет", "2-е послание Петра"],
                     ["1иоанна", "1ин", "1-е послание Иоанна"],
                     ["2иоанна", "2ин", "2-е послание Иоанна"],
                     ["3иоанна", "3ин", "3-е послание Иоанна"],
                     ["иуды", "иуд", "1-е послание Иуды"],
                     ["римлянам", "рим", "Послание римлянам"],
                     ["1коринфянам", "1кор", "1-е послание коринфянам"],
                     ["2коринфянам", "2кор", "2-е послание коринфянам"],
                     ["галатам", "гал", "Послание галатам"],
                     ["ефесянам", "еф", "Послание ефесянам"],
                     ["филиппийцам", "флп", "Послание филиппийцам"],
                     ["колоссянам", "кол", "Послание колоссянам"],
                     ["1фессалоникийцам", "1фес", "1-е послание фессалоникийцам"],
                     ["2фессалоникийцам", "2фес", "2-е послание фессалоникийцам"],
                     ["1тимофею", "1тим", "1-е послание Тимофею"],
                     ["2тимофею", "2тим", "2-е послание Тимофею"],
                     ["титу", "тит", "Послание Титу"],
                     ["филимону", "флм", "Послание Филимону"],
                     ["евреям", "евр", "Послание евреям"],
                     ["откровение", "откр", "Откровение Иоанна Богослова"]]

# *** Ключ для списка доступных каналов в словаре конфига
UNIT_ID = "theolog"

# *** Команды поиска текста по книгам Библии
NEW_TESTAMENT: str = "найтинз"
OLD_TESTAMENT: str = "найтивз"
NEW_TESTAMENT_ENG: str = "findnew"
OLD_TESTAMENT_ENG: str = "findold"
FIND_IN_BOOK: str = "найти"
FIND_IN_BOOK_ENG: str = "find"
OLD_TESTAMENT_BOOKS = range(1, 40)
NEW_TESTAMENT_BOOKS = range(40, 67)

THEOLOG_HINT: list = ["библия", "bible"]
THEOLOG_HELP: list = ["книги", "books", f"{OLD_TESTAMENT}", f"{NEW_TESTAMENT}", 
                      f"{OLD_TESTAMENT_ENG}", f"{NEW_TESTAMENT_ENG}", f"{FIND_IN_BOOK}", f"{FIND_IN_BOOK_ENG}" ]
MAX_SEARCH_RESULT: int = 4
OUTPUT_COUNT = "-n"
FULL_OUTPUT = "-f"
# !найтивз/нз фраза
# !найти книга фраза
# !книга глава кол-во строк


def search_in_book(pbook_file: str, pbook_title: str, pphrase: str):
    """Ищет заданную строку в заданном файле."""

    result_list: list = []
    with open(pbook_file, "r", encoding="utf-8") as book_file:

        for line in book_file:

            lower_line = line.lower()
            parsed_line = re.split(r':', lower_line, maxsplit=2)
            joined_line: str = " ".join(parsed_line[2:])
            if pphrase in joined_line:

                parsed_line = re.split(r':', line, maxsplit=2)
                result_line: str = " ".join(parsed_line[2:])
                result_list.append(f"{pbook_title} глава {parsed_line[0]} стих "
                                   f"{parsed_line[1]}: {result_line}")
            if len(result_list) > MAX_SEARCH_RESULT:

                break
    return "\n".join(result_list)


class CTheolog(prototype.CPrototype):
    """Класс теолога."""

    def __init__(self, pconfig: dict, pdata_path):
        """"Конструктор."""

        super().__init__()
        self.config: dict = pconfig
        self.data_path: str = pdata_path + THEOLOG_FOLDER


    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если теолог может обработать эту команду."""

        assert pchat_title is not None, \
            "Assert: [theolog.can_process] No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [theolog.can_process] No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            if word_list[0].lower() in THEOLOG_HELP or word_list[0].lower() in THEOLOG_HINT:

                return True

            for book in BIBLE_BOOKS:

                if word_list[0].lower() in book:

                    return True
        return False


    def find_in_book(self, pbook_idx: int, pbook_name: str, pchapter: str, pverse: str,
                     poutput_count: int) -> str:  # noqa
        """Ищет заданную строку в файле."""

        assert pbook_idx is not None, \
            "Assert: [theolog.find_in_book] No <pbook_idx> parameter specified!"
        assert pverse is not None, \
            "Assert: [theolog.find_in_book] No <pverse> parameter specified!"
        assert pbook_name is not None, \
            "Assert: [theolog.find_in_book] No <pbook> parameter specified!"
        assert poutput_count is not None, \
            "Assert: [theolog.find_in_book] No <pline_count> parameter specified!"
        answer: str = ""
        # *** Путь к файлу
        book_file_name: str = f"{self.data_path}{pbook_idx + 1}.txt"
        # *** Если номер строки пустой, берем первый
        if not pverse.strip():

            pverse = "1"
        line_id: str = f"{pchapter}:{pverse}:"
        # *** Открываем нужную книгу и перебираем её
        with open(book_file_name, "r", encoding="utf-8") as book_file:
    
            for line in book_file:

                # *** Ищем в файле заданный идентификатор строки
                if re.search(f"^{line_id}", line) is not None:

                    text_pos: int = line.find(':', line.find(':') + 1)
                    result: str = line[:text_pos] + " " + line[text_pos+1:]
                    answer = f"{pbook_name} {result}"
                    if poutput_count == 1:

                        break
                # *** Если что-то нашлось в предыдущей итерации..        
                elif answer:

                    # *** и нужно выдать больше одной строки...
                    if poutput_count > 1:

                        # *** Добавляем их в ответ
                        parsed_line: list = line.split(":")
                        answer += "\n" + parsed_line[2]
                        poutput_count -= 1
                    else:

                        break
        return answer


    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд, поддерживаемых модулем."""
        
        if self.is_enabled(pchat_title):
            
            return ", ".join(THEOLOG_HELP)
        return None


    def get_books(self, pchat_title: str) -> str:
        """Возвращает список книг Библии."""

        books: str = ""
        if self.is_enabled(pchat_title):

            for book in BIBLE_BOOKS:

                if not book[0][0].isdigit():

                    books += f"{book[0].capitalize()}({book[1]}), "
                else:

                    books += f"{book[0]}({book[1]}), "
        return books


    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем."""

        assert pchat_title is not None, \
            "Assert: [theolog.get_hint] " \
            "No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):

            # hint: list = THEOLOG_HINT
            # hint[2] += " [-nX] [-f]"
            # hint[3] += " [-nX] [-f]"
            # hint[4] += " книга фрагмент"
            # hint.append("книга [-nX] глава стих")
            return ", ".join(THEOLOG_HINT)
        return ""


    def global_search(self, ptestament: str, pphrase: str,
                      pfull_output: bool = False, poutput_count: int = 0) -> str:  # noqa
        """Ищет заданную строку по всем книгам заданного завета"""

        assert ptestament is not None, \
            "Assert: [theolog.global_search] No <ptestament> parameter specified!"
        assert pphrase is not None, \
            "Assert: [theolog.global_search] No <pphrase> parameter specified!"
        result_list: list = []
        parsed_line: list
        answer: str = ""
        # *** По умолчанию берем Ветхий Завет
        search_range = OLD_TESTAMENT_BOOKS
        # *** Если нужен Новый - выбираем его
        if ptestament == NEW_TESTAMENT:

            search_range = NEW_TESTAMENT_BOOKS
        # *** Перебираем книги в заданном диапазоне    
        for book in search_range:

            # *** Берем полное наименование книги
            book_title: str = BIBLE_BOOKS[book-1][2]
            # *** И название файла книги
            book_name = f"{self.data_path}{book}.txt"
            # *** Открываем файл и экшен!
            with open(book_name, "r", encoding="utf-8") as book_file:

                for line in book_file:

                    lower_line = line.lower()
                    # *** Если искомая фраза содержится в строке...
                    if pphrase in lower_line:

                        # *** Парсим строчку на три части
                        parsed_line = re.split(r'\:', line, maxsplit=2)
                        # *** Формируем ответ
                        result_list.append(f"{book_title} глава {parsed_line[0]}"
                                           f" стих {parsed_line[1]} : {parsed_line[2]}")
        # *** Если что-то нашли и ответ готов...
        if len(result_list) > 0:

            if pfull_output:

                answer = "\n".join(result_list)
            elif poutput_count > 0:

                if len(result_list) < poutput_count:

                    poutput_count = len(result_list)
                answer = "\n".join(result_list[:poutput_count])
            else:

                answer = random.choice(result_list)
        return answer


    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если бармен разрешен на этом канале."""

        assert pchat_title is not None, \
            "Assert: [theolog.is_enabled] No <pchat_title> parameter specified!"
        if pchat_title in self.config["chats"]:

            return UNIT_ID in self.config["chats"][pchat_title]
        return False


    def reload(self):
        pass


    def theolog(self, pchat_title: str, pmessage_text: str) -> str:
        """Обрабатывает запросы теолога."""

        assert pchat_title is not None, \
            "Assert: [theolog.theolog] No <pchat_title> parameter specified!"
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text.replace(":", " "))
        verse: str = ""
        param_count = len(word_list)
        book_name: str
        chapter: str = ""
        full_result: bool = False
        output_count: int = 1

        # *** Можем обработать?
        if self.can_process(pchat_title, pmessage_text):

            # *** Если есть один параметр, то запрос помощи должен быть это
            if (param_count == 1):
                
                if word_list[COMMAND_ARG] in THEOLOG_HINT:

                    return self.get_help(pchat_title)
                # *** Либо запрос списка книг
                print(f"@@@ {word_list[COMMAND_ARG]}")
                print(f"@@@ {THEOLOG_HELP[0:2]}")
                if word_list[COMMAND_ARG] in THEOLOG_HELP[0:2]:
                
                    return self.get_books(pchat_title)
            # *** Если есть два параметра, то это книга и глава/стих.
            if param_count > 1:

                # *** Если первый параметр - команда поиска...
                if word_list[0].lower() in [NEW_TESTAMENT, OLD_TESTAMENT]:

                    # *** ..получим команду.
                    testament = word_list[0]

                    # *** Нет ли там параметров выдачи?
                    for word in word_list:

                        full_result = FULL_OUTPUT in word
                        if full_result:

                            word_list.remove(word)
                            break
                        if OUTPUT_COUNT in word:

                            output_count = int(word[2:])
                            word_list.remove(word)
                            break

                    phrase = " ".join(word_list[1:]).lower()
                    answer = self.global_search(testament, phrase, full_result, output_count)
                elif word_list[0].lower() == FIND_IN_BOOK:

                    # *** Искать в книге
                    book_name = word_list[1]
                    book_index: int = -1
                    for index, book in enumerate(BIBLE_BOOKS):

                        if book_name.lower() in book:

                            book_index = index
                            break
                    if book_index >= 0:

                        book_file = f"{self.data_path}/{book_index+1}.txt"
                        answer = search_in_book(book_file, BIBLE_BOOKS[book_index][2],
                                                " ".join(word_list[2:]))
                else:

                    # *** Книгу и главу
                    book_name = word_list[0].lower()
                    book_idx: int = 0
                    # *** Переберем всё
                    for idx, book in enumerate(BIBLE_BOOKS):

                        if book_name in book:

                            book_idx = idx
                            book_name = book[2]
                            break
                    for word in word_list:

                        # *** Если задано количество...
                        if OUTPUT_COUNT in word:

                            output_count = int(word[2:])
                            word_list.remove(word)
                            break

                    # *** Есть второй параметр, то это глава
                    if (len(word_list) > 1) and word_list[1].isdigit():

                        chapter = word_list[1]
                    # *** Есть третий параметр, то это стих
                    if (len(word_list) > 2) and word_list[2].isdigit():

                        verse = word_list[2]

                    answer = self.find_in_book(book_idx, book_name, chapter, verse, output_count)
                    if not answer:

                        answer = "Нет такой главы и/или стиха в этой книге."
            if len(answer) > 0:

                print(f"Theolog answers: {answer[:func.OUT_MSG_LOG_LEN]}...")
            else:

                answer = "Ничего не нашёл."
        return answer[:1024]
