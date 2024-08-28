#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Игровой модуль."""


import random
import typing as type
import prototype
import functions as func

UNIT_ID: str = "gambler"
HINT: type.Tuple(str) = ("игра", "game")
GAMBLER_COMMANDS: type.Tuple(str) = ("камень", "ножницы", "бумага")
GAMBLER_SHORT_COMMANDS: type.Tuple(str) = ("кам", "нож", "бум")
ROCK_COMMAND: int = 0
SCISSORS_COMMAND: int = 1
PAPER_COMMAND: int = 2

class CGambler(prototype.CPrototype):
    """Класс библиотекаря."""

    def __init__(self, pconfig: dict, pdata_path: str):

        super().__init__()
        self.config = pconfig
        # self.data_path = pdata_path + LIBRARIAN_FOLDER
        # self.quotes: list = []
        # self.reload()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если библиотекарь может обработать эту команду."""
        assert pchat_title is not None, \
            "Assert: [librarian.can_process] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [librarian.can_process] " \
            "Пропущен параметр <pmessage_text> !"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in GAMBLER_COMMANDS:

                found = word_list[0] in command
                if found:

                    break
            if not found:

                found = word_list[0] in HINT
        return found


    def get_help(self, pchat_title: str) -> str:
        """Пользователь запросил список команд."""
        assert pchat_title is not None, \
            "Assert: [librarian.get_help] " \
            "No <pchat_title> parameter specified!"
        command_list: str = ""
        if self.is_enabled(pchat_title):

            for command in GAMBLER_COMMANDS:

                command_list += ", ".join(command)
                command_list += "\n"
        return command_list


    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [librarian.get_hint] " \
            "Пропущен параметр <pchat_title> !"
        if self.is_enabled(pchat_title):

            return ", ".join(HINT)
        return ""


    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если библиотекарь разрешен на этом канале."""
        assert pchat_title is not None, \
            "Assert: [librarian.is_enabled] " \
            "Пропущен параметр <pchat_title> !"
        return UNIT_ID in self.config["chats"][pchat_title]


    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:

            return True, ""
        # *** Низзя
        print(f"> Librarian: Запрос на удаление цитаты от нелегитимного лица {puser_title}.")
        return False, f"У вас нет на это прав, {puser_title}."


    def gambler(self, pchat_title, puser_name: str, puser_title: str, pmessage_text: str):
        """Основной метод класса."""

        command: int
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            else:

                # *** Получим код команды
                if word_list[0] in GAMBLER_COMMANDS:

                    command = GAMBLER_COMMANDS.index(word_list[0])
                elif word_list[0] in GAMBLER_SHORT_COMMANDS:

                    command = GAMBLER_SHORT_COMMANDS.index(word_list[0])
                else:

                    command = -1
            if command >= 0:

                answer = f"Ваш выбор {GAMBLER_COMMANDS[command]}\n"
                turn = random.randint(0,3)
                if command == turn:

                    answer += f"Я выбрал также {GAMBLER_COMMANDS[command]}. Ничья."
                else:

                    answer += f"Мой выбор {GAMBLER_COMMANDS[turn]}."
                    if turn == ROCK_COMMAND:

                        # *** Камень
                        if command == SCISSORS_COMMAND:

                            answer += " Вы проиграли."
                        else:

                            answer += " Вы выиграли."
                    elif turn == SCISSORS_COMMAND:

                        # *** Ножницы
                        if command == PAPER_COMMAND:

                            answer +=  " Вы проиграли."
                        else:

                            answer += " Вы выиграли."
                    else:

                        # *** Бумага.
                        if command == ROCK_COMMAND:

                            answer +=  " Вы проиграли."
                        else:

                            answer += " Вы выиграли."

            else:

                answer = f"Я не знаю такой игры"
            if answer:

                print("> Gambler отвечает: ", answer[:func.OUT_MSG_LOG_LEN])

        return answer


