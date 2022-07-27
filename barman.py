# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль бармена."""

import random

import functions as func
import prototype

# *** Список списков доступных команд
COMMANDS: list = [["пиво", "beer", "пв", "br"],  # ***
                  ["водка", "vodka", "вк", "vk"],
                  ["коньяк", "cognac", "кн", "cn"],
                  ["коктейль", "cocktail", "кт", "ct"],
                  ["чай", "tea", "чй", "te"],
                  ["кофе", "coffee", "кф", "cf"],
                  ["печеньки", "cookies", "пч", "ck"],
                  ["шоколад", "chocolate", "шк", "ch"]]

# *** Идентификаторы, они же индексы, напитков, их ключи и эмодзи
ID_KEY: str = "id"
PROPERTIES_KEY: str = "keys"  # ***
EMODJI_KEY: str = "emodji"  # ***
COMMAND_KEY: str = "command"  # ***
SOURCES_KEY: str = "sources"  # ***
MARKS_KEY: str = "marks"  # ***
CANS_KEY: str = "cans"  # ***
FILLS_KEY: str = "fills"  # ***
TRANSFER_KEY: str = "transfer"  # ***
TEMPLATE_KEY: str = "template"  # ***

BEER_ID: int = 0  # ***
VODKA_ID: int = 1  # ***
COGNAC_ID: int = 2  # ***
COCKTAIL_ID: int = 3  # ***
TEA_ID: int = 4  # ***
COFFEE_ID: int = 5  # ***
COOKIE_ID: int = 6  # ***
CHOCOLATE_ID: int = 7  # ***

ASSORTIMENT: tuple = ({ID_KEY: BEER_ID,
                       EMODJI_KEY: "🍺",
                       COMMAND_KEY: COMMANDS[BEER_ID],
                       SOURCES_KEY: "drink_sources.txt",
                       CANS_KEY: "beer_cans.txt",
                       MARKS_KEY: "beer_marks.txt",
                       TRANSFER_KEY: "drink_transfer.txt",
                       PROPERTIES_KEY: (SOURCES_KEY, CANS_KEY, MARKS_KEY, TRANSFER_KEY),
                       TEMPLATE_KEY: "Softice {0} {1} пива \"{2}\" {3} {4} {5}"},
                      # TEMPLATE_KEY: "Softice {source} {can} пива \"{mark}\"
                      # {transfer} {puser_name} {BEER_EMODJI}"},
                      {ID_KEY: VODKA_ID,
                       EMODJI_KEY: "🍸",
                       COMMAND_KEY: COMMANDS[VODKA_ID],
                       SOURCES_KEY: "drink_sources.txt",
                       CANS_KEY: "vodka_cans.txt",
                       MARKS_KEY: "vodka_marks.txt",
                       FILLS_KEY: "vodka_fills.txt",
                       PROPERTIES_KEY: (SOURCES_KEY, CANS_KEY, MARKS_KEY, FILLS_KEY),
                       TEMPLATE_KEY: "Softice {0} {1} {2} и {3} {4} {5}"},
                      {ID_KEY: COGNAC_ID,
                       EMODJI_KEY: "🥃",
                       COMMAND_KEY: COMMANDS[COGNAC_ID],
                       SOURCES_KEY: "drink_sources.txt",
                       CANS_KEY: "cognac_cans.txt",
                       MARKS_KEY: "cognac_marks.txt",
                       FILLS_KEY: "cognac_fills.txt",
                       PROPERTIES_KEY: (SOURCES_KEY, CANS_KEY, MARKS_KEY, FILLS_KEY),
                       TEMPLATE_KEY: "Softice {0} {1} {2} и {3} {4} {5}"},
                      {ID_KEY: COCKTAIL_ID,
                       EMODJI_KEY: "🍹",
                       COMMAND_KEY: COMMANDS[COCKTAIL_ID],
                       SOURCES_KEY: "drink_sources.txt",
                       MARKS_KEY: "cocktail_marks.txt",
                       FILLS_KEY: "cocktail_fills.txt",
                       PROPERTIES_KEY: (SOURCES_KEY, MARKS_KEY, FILLS_KEY),
                       TEMPLATE_KEY: "Softice {0} {1} и {2} {3} {4}"},
                      {ID_KEY: TEA_ID,
                       EMODJI_KEY: "🫖",
                       COMMAND_KEY: COMMANDS[TEA_ID],
                       FILLS_KEY: "tea_fills.txt",
                       MARKS_KEY: "tea_marks.txt",
                       TRANSFER_KEY: "drink_transfer.txt",
                       PROPERTIES_KEY: (FILLS_KEY, MARKS_KEY, TRANSFER_KEY),
                       TEMPLATE_KEY: "Softice {0} {1} {2} {3} {4}"},
                      {ID_KEY: COFFEE_ID,
                       EMODJI_KEY: "☕️",
                       COMMAND_KEY: COMMANDS[COFFEE_ID],
                       TRANSFER_KEY: "drink_transfer.txt",
                       MARKS_KEY: "coffee_marks.txt",
                       FILLS_KEY: "coffee_fills.txt",
                       PROPERTIES_KEY: (FILLS_KEY, MARKS_KEY, TRANSFER_KEY),
                       TEMPLATE_KEY: "Softice {0} кофе \"{1}\" {2} {3} {4}"},
                      {ID_KEY: COOKIE_ID,
                       EMODJI_KEY: "🍪",
                       COMMAND_KEY: COMMANDS[COOKIE_ID],
                       SOURCES_KEY: "cookies_sources.txt",
                       MARKS_KEY: "cookies_marks.txt",
                       TRANSFER_KEY: "cookies_transfer.txt",
                       PROPERTIES_KEY: (SOURCES_KEY, MARKS_KEY, TRANSFER_KEY),
                       TEMPLATE_KEY: "Softice {0} печенье \"{1}\" {2} {3} {4}"},
                      {ID_KEY: CHOCOLATE_ID,
                       EMODJI_KEY: "🍫",
                       COMMAND_KEY: COMMANDS[CHOCOLATE_ID],
                       SOURCES_KEY: "chocolate_sources.txt",
                       MARKS_KEY: "chocolate_marks.txt",
                       TRANSFER_KEY: "chocolate_transfer.txt",
                       PROPERTIES_KEY: (SOURCES_KEY, MARKS_KEY, TRANSFER_KEY),
                       TEMPLATE_KEY: "Softice {0} {1} {2} {3} {4}"})

# *** Команда перегрузки текстов
BAR_RELOAD: list = ["barreload", "barl"]
BARMAN_FOLDER: str = "barman/"
# *** Ключ для списка доступных каналов в словаре конфига
ENABLED_IN_CHATS_KEY: str = "barman_chats"
BAR_HINT: list = ["бар", "bar"]


class CBarman(prototype.CPrototype):
    """Класс бармена."""

    def __init__(self, pconfig, pdata_path):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + BARMAN_FOLDER
        self.bar_content: dict = {}
        self.load_assortiment()

    def barman(self, pchat_title: str, pmessage_text: str, puser_title: str) -> str:
        """Процедура разбора запроса пользователя."""
        assert pchat_title is not None, \
            "Assert: [barman.barman] No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [barman.barman] No <puser_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [barman.barman] No <pmessage_text> parameter specified!"
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили меню.
            if word_list[0] in BAR_HINT:

                answer = "Сегодня в баре имеется следующий ассортимент: \n" + \
                         self.get_help(pchat_title)
            elif word_list[0] in BAR_RELOAD:

                self.load_assortiment()
                print("Barman successfully reload bar assortiment.")
                answer = "Содержимое бара обновлено"
            else:

                answer = self.serve_client(puser_title, word_list[0])
        if answer:
            print(f"Barman answers: {answer[:16]}")
        return answer

    def serve_client(self, puser_name: str, pcommand: str):
        """Обслуживает клиентов."""
        answer: str = ""
        for item in ASSORTIMENT:

            # print(item[COMMAND_KEY], pcommand)
            if pcommand in item[COMMAND_KEY]:

                # *** Замечательно, мы нашли, что попросил клиент.
                # *** Нужно сформировать список параметров для
                #     функции format
                arguments: list = []
                for prop in item[PROPERTIES_KEY]:

                    arguments.append(random.choice(self.bar_content[item[ID_KEY]][prop]))
                # *** Предпоследний аргумент - имя пользователя
                arguments.append(puser_name)
                # *** Последний аргумент - это эмоджи
                arguments.append(item[EMODJI_KEY])

                # *** Ок, формируем ответ
                answer: str = item[TEMPLATE_KEY].format(*arguments)
        return answer

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если бармен может обработать эту команду"""
        assert pchat_title is not None, \
            "Assert: [barman.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [barman.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in COMMANDS:

                found = word_list[0] in command
                if found:
                    break
            if not found:

                found = word_list[0] in BAR_HINT
                if not found:
                    found = word_list[0] in BAR_RELOAD
        return found

    def get_help(self, pchat_title: str) -> str:  # noqa
        """Пользователь запросил список команд."""
        command_list: str = ""
        if self.is_enabled(pchat_title):

            for command in COMMANDS:

                for kind in command:
                    command_list += kind + ", "
                command_list = command_list[:-2]
                command_list += "\n"
        return command_list

    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [barman.get_hint] " \
            "No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):
            return ", ".join(BAR_HINT)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если бармен разрешен на этом канале.
        >>> self.is_enabled({'barman_chats':'Ботовка'}, 'Ботовка')
        True
        >>> self.is_enabled({'barman_chats':'Хокку'}, 'Ботовка')
        False
        """
        assert pchat_title is not None, \
            "Assert: [barman.is_enabled] " \
            "No <pchat_title> parameter specified!"

        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def load_assortiment(self):
        """Загружает ассортимент бара."""
        # print(ASSORTIMENT[0])
        for item in ASSORTIMENT:

            self.load_item(item)
        print(f"Barman successfully loaded {len(ASSORTIMENT)} items")

    def load_item(self, pitem: dict):  # pmainkey: str, pkeys: tuple, pproperties: dict):
        """Загружает одно наименование ассортимента бара."""
        storage: dict = {}
        for key in pitem[PROPERTIES_KEY]:

            storage[key] = func.load_from_file(self.data_path + pitem[key])

        self.bar_content[pitem[ID_KEY]] = storage

    def reload(self):
        """Перегружает все содержимое бара."""
