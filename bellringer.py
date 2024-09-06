# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль для бота."""

import functions as func
import prototype

COMMANDS: list = ["звонить", "звон", "зв", "ring"]
BELLRINGER_HINT: list = ["звонарь", "ringer"]
BELLRINGER_FOLDER: str = "bellringer/"
UNIT_ID = "bellringer"
TOAD_COMMANDS = ["данж", "туса"]
DUNGEON_COMMAND = 0
TOAD_CHANNELS = ["OSQ Жабки"]
MAFIA_CHANNELS = ["Maftown", "Mafia City"]


class CBellRinger(prototype.CPrototype):
    """Класс звонаря."""

    def __init__(self, pconfig, pdata_path):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + BELLRINGER_FOLDER

    def bellringer(self, pchat_title: str, pmessage_text: str):
        """Основная функция модуля."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in BELLRINGER_HINT:

                answer = self.get_help(pchat_title)
            else:

                # print(word_list[0], COMMANDS)
                if word_list[0] in COMMANDS:

                    if pchat_title in MAFIA_CHANNELS:

                        user_list = func.load_from_file(self.data_path+"/"+pchat_title+".txt")
                        answer = "Эй, " + ", ".join(user_list) + \
                                 "! Пошли, поохотимся на дона! или на мителей..."
                elif word_list[0] in TOAD_COMMANDS:

                    if pchat_title in TOAD_CHANNELS:

                        user_list = func.load_from_file(self.data_path+"/"+pchat_title+".txt")
                        answer = "Эй, " + ", ".join(user_list)
                        if word_list[0] == TOAD_COMMANDS[DUNGEON_COMMAND]:

                            answer += ", пошли в рейд! Подземелье ждёт!"
                        else:

                            answer += ", пошли потусим!"
        if answer:

            print(f"BellRinger отвечает: {answer[:func.OUT_MSG_LOG_LEN]}")
        return answer

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            cmd_list: list = []
            cmd_list.extend(COMMANDS)
            cmd_list.extend(TOAD_COMMANDS)
            for command in cmd_list:

                found = word_list[0] in command
                if found:

                    break
            if not found:

                found = word_list[0] in BELLRINGER_HINT
        return found

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return ", ".join(COMMANDS) + ", ".join(TOAD_COMMANDS) + "\n"

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        if self.is_enabled(pchat_title):

            return ", ".join(BELLRINGER_HINT)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return UNIT_ID in self.config["chats"][pchat_title]
        # return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        return puser_name == self.config["master"]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
