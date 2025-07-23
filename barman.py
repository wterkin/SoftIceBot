# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль бармена."""

import random

import functions as func
import prototype

# *** Список списков доступных команд
COMMANDS: list = [["пиво", "beer", "пв", "br"],
                  ["водка", "vodka", "вк", "vk"],
                  ["коньяк", "cognac", "кн", "cn"],
                  ["коктейль", "cocktail", "кт", "ct"],
                  ["чай", "tea", "чй", "te"],
                  ["кофе", "coffee", "кф", "cf", "кофи"],
                  ["печеньки", "cookies", "пч", "ck"],
                  ["шоколад", "chocolate", "шк", "ch"],
                  ["мороженое", "icecream", "мр", "ic"],
                  ["булочка", "bun", "бч", "bn"],
                  ["шампанское", "champagne", "шмп", "chm"],
                  ]

# *** Идентификаторы, они же индексы, напитков, их ключи и эмодзи
ID_KEY: str = "id"
PROPERTIES_KEY: str = "properties"
EMODJI_KEY: str = "emodji"
COMMAND_KEY: str = "command"
SOURCES_KEY: str = "sources"
MARKS_KEY: str = "marks"
CANS_KEY: str = "cans"
FILLS_KEY: str = "fills"
TRANSFER_KEY: str = "transfer"
TEMPLATE_KEY: str = "template"

BEER_ID: int = 0
VODKA_ID: int = 1
COGNAC_ID: int = 2
COCKTAIL_ID: int = 3
TEA_ID: int = 4
COFFEE_ID: int = 5
COOKIE_ID: int = 6
CHOCOLATE_ID: int = 7
ICECREAM_ID: int = 8
BUN_ID: int = 9
CHAMPAGNE_ID: int = 10


ASSORTMENT: tuple = ({ID_KEY: BEER_ID,
                      EMODJI_KEY: "🍺",
                      COMMAND_KEY: COMMANDS[BEER_ID],
                      SOURCES_KEY: "drink_sources.txt",
                      CANS_KEY: "beer_cans.txt",
                      MARKS_KEY: "beer_marks.txt",
                      TRANSFER_KEY: "drink_transfer.txt",
                      PROPERTIES_KEY: (SOURCES_KEY, CANS_KEY, MARKS_KEY, TRANSFER_KEY),
                      TEMPLATE_KEY: "Softice {0} {1} пива \"{2}\" {3} {4} {5}"},
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
                      TEMPLATE_KEY: "Softice {0} {1} {2} {3} {4}"},
                     {ID_KEY: ICECREAM_ID,
                      EMODJI_KEY: "🍦",
                      COMMAND_KEY: COMMANDS[ICECREAM_ID],
                      SOURCES_KEY: "icecream_sources.txt",
                      MARKS_KEY: "icecream_marks.txt",
                      TRANSFER_KEY: "icecream_transfer.txt",
                      PROPERTIES_KEY: (SOURCES_KEY, MARKS_KEY, TRANSFER_KEY),
                      TEMPLATE_KEY: "Softice {0} {1} {2} {3} {4}"},
                     {ID_KEY: BUN_ID,
                      EMODJI_KEY: "🥨🥯🥯🥯🥯",
                      COMMAND_KEY: COMMANDS[BUN_ID],
                      SOURCES_KEY: "bun_sources.txt",
                      MARKS_KEY: "bun_marks.txt",
                      TRANSFER_KEY: "bun_transfer.txt",
                      PROPERTIES_KEY: (SOURCES_KEY, MARKS_KEY, TRANSFER_KEY),
                      TEMPLATE_KEY: "Softice {0} {1} {2} {3} {4}"},
                      {ID_KEY: CHAMPAGNE_ID,
                      EMODJI_KEY: "🍾",
                      COMMAND_KEY: COMMANDS[CHAMPAGNE_ID],
                      SOURCES_KEY: "drink_sources.txt",
                      CANS_KEY: "champ_cans.txt",
                      MARKS_KEY: "champ_marks.txt",
                      TRANSFER_KEY: "drink_transfer.txt",
                      PROPERTIES_KEY: (SOURCES_KEY, CANS_KEY, MARKS_KEY, TRANSFER_KEY),
                      TEMPLATE_KEY: "Softice {0} {1} шампанского \"{2}\" {3} {4} {5}"},
                     )

# *** Команда перегрузки текстов
BAR_HINT: list = ["бар", "bar"]
BAR_RELOAD: list = ["brreload", "brrl"]
BARMAN_FOLDER: str = "barman/"
# *** Ключ для списка доступных каналов в словаре конфига
UNIT_ID = "barman"


class CBarman(prototype.CPrototype):
    """Класс бармена."""

    def __init__(self, pconfig, pdata_path):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + BARMAN_FOLDER
        self.bar_content: dict = {}
        self.load_assortment()


    def barman(self, pchat_title: str, puser_name: str, puser_title: str,
               pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""
        assert pchat_title is not None, \
            "Assert: [barman.barman] Пропущен параметр <pchat_title> !"
        assert puser_title is not None, \
            "Assert: [barman.barman] Пропущен параметр <puser_title> !"
        assert pmessage_text is not None, \
            "Assert: [barman.barman] Пропущен параметр <pmessage_text> !"

        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили меню.
            if word_list[0] in BAR_HINT:

                answer = "Сегодня в баре имеется следующий ассортимент: \n" + \
                         self.get_help(pchat_title)
            elif word_list[0] in BAR_RELOAD:

                if self.is_master(puser_name):

                    self.reload()
                    answer = "Ассортимент бара обновлён."
                else:

                    print(f"> Barman: Запрос на перезагрузку бара от "
                          f"нелегитимного лица {puser_title}.")
                    answer = f"У вас нет на это прав, {puser_title}."
            else:

                if len(word_list) > 1:

                    answer = self.serve_client(" ".join(word_list[1:]), word_list[0])
                else:

                    answer = self.serve_client(puser_title, word_list[0])
        if answer:

            print(f"> Barman отвечает: {answer[:func.OUT_MSG_LOG_LEN]}")
        return answer.strip()


    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если бармен может обработать эту команду"""
        assert pchat_title is not None, \
            "Assert: [barman.can_process] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [barman.can_process] " \
            "Пропущен параметр <pmessage_text> !"

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
        assert pchat_title is not None, \
            "Assert: [barman.get_help] " \
            "Пропущен параметр <pchat_title> !"

        command_list: str = ""
        if self.is_enabled(pchat_title):

            for command in COMMANDS:

                command_list += ", ".join(command) + "\n"
        return command_list


    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [barman.get_hint] " \
            "Пропущен параметр <pchat_title> !"

        if self.is_enabled(pchat_title):

            return ", ".join(BAR_HINT)
        return ""


    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если бармен разрешен на этом канале."""
        assert pchat_title is not None, \
            "Assert: [barman.is_enabled] " \
            "Пропущен параметр <pchat_title> !"

        return UNIT_ID in self.config["chats"][pchat_title]


    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""

        return puser_name == self.config["master"]

    def load_assortment(self):
        """Загружает ассортимент бара."""

        for item in ASSORTMENT:

            self.load_item(item)
        print(f"> Barman успешно (пере)загрузил {len(ASSORTMENT)} типов товаров.")

    def load_item(self, pitem: dict):
        """Загружает одно наименование ассортимента бара."""
        assert pitem is not None, \
            "Assert: [barman.load_item] " \
            "Пропущен параметр <pitem> !"

        storage: dict = {}
        for key in pitem[PROPERTIES_KEY]:

            storage[key] = func.load_from_file(self.data_path + pitem[key])
        self.bar_content[pitem[ID_KEY]] = storage


    def reload(self):  # , pchat_id: int, puser_name: str, puser_title):
        """Перегружает все содержимое бара."""

        self.load_assortment()

    def serve_client(self, puser_name: str, pcommand: str):
        """Обслуживает клиентов."""
        assert puser_name is not None, \
            "Assert: [barman.serve_client] Пропущен параметр <puser_name> !"
        assert pcommand is not None, \
            "Assert: [barman.serve_client] Пропущен параметр <pcommand> !"

        answer: str = ""
        for item in ASSORTMENT:

            if pcommand.strip() in item[COMMAND_KEY]:

                arguments: list = []
                for prop in item[PROPERTIES_KEY]:

                    arguments.append(random.choice(self.bar_content[item[ID_KEY]][prop]))
                # *** Предпоследний аргумент - имя пользователя
                arguments.append(puser_name)
                # *** Последний аргумент - это эмоджи
                arguments.append(item[EMODJI_KEY])
                # *** Ок, формируем ответ
                answer = item[TEMPLATE_KEY].format(*arguments)
        return answer
