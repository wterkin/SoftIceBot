# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль звонаря."""

import functions as func
import prototype

COMMANDS: list = ["звонить", "звон", "зв", "ring", "игрок+", "игр+", "игрок-", "игр-"]
BELLRINGER_HINT: list = ["звонарь", "ringer"]
BELLRINGER_FOLDER: str = "bellringer/"
UNIT_ID: str = "bellringer"
MAFIA_CHANNELS: list = ["Асы мафии", "TestPlace"]
RING_CMDS_OFFSET: int = 0
ADD_PLAYER_CMDS_OFFSET: int = 4
DEL_PLAYER_CMDS_OFFSET: int = 6

class CBellRinger(prototype.CPrototype):
    """Класс звонаря."""

    def __init__(self, pconfig, pdata_path):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + BELLRINGER_FOLDER


    def bellringer(self, pchat_title: str, puser_name: str, pmessage_text: str):
        """Основная функция модуля."""

        answer: str = ""
        player_list: list
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in BELLRINGER_HINT:

                answer = self.get_help(pchat_title)
            else:

                if word_list[0] in COMMANDS:

                    if word_list[0] in COMMANDS[ADD_PLAYER_CMDS_OFFSET:ADD_PLAYER_CMDS_OFFSET+2]:

                        # *** Пользователь хочет добавить игрока
                        if self.is_master(puser_name):

                            file_name:str = self.data_path+pchat_title+".txt"
                            player_list = func.load_from_file(file_name)
                            player_name: str = word_list[1]
                            if player_name not in player_list:

                                player_list.append(player_name)
                                func.save_list(player_list, file_name)
                                answer = f"Игрок {player_name} добавлен."
                            else:

                                answer = f"Игрок {player_name} уже есть в списке."
                    elif word_list[0] in COMMANDS[DEL_PLAYER_CMDS_OFFSET:DEL_PLAYER_CMDS_OFFSET+2]:

                        # *** Пользователь хочет удалить игрока
                        if self.is_master(puser_name):

                            player_name: str = word_list[1]
                            file_name: str = self.data_path+"/"+pchat_title+".txt"
                            player_list = func.load_from_file(file_name)
                            if player_name in player_list:

                                try:
                                    player_idx = player_list.index(player_name)
                                except ValueError:
                                    player_idx = -1
                                if player_idx >= 0:

                                    del player_list[player_idx]
                                    func.save_list(player_list, file_name)
                                    answer = f"Игрок {player_name} удален"
                            else:

                                answer = f"Игрок {player_name} отсутствует в списке"
                    elif word_list[0] in COMMANDS[RING_CMDS_OFFSET:RING_CMDS_OFFSET+4]:

                        if pchat_title in MAFIA_CHANNELS:

                            user_list = func.load_from_file(self.data_path+"/"+pchat_title+".txt")
                            answer = "Эй, " + ", ".join(user_list) + \
                                     "! Пошли, поохотимся на дона! или на мителей..."
        if answer:

            print(f"BellRinger отвечает: {answer[:func.OUT_MSG_LOG_LEN]}")
        return answer


    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""

        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in COMMANDS:

                found = word_list[0] in command
                if found:

                    break
            if not found:

                found = word_list[0] in BELLRINGER_HINT
        return found


    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""

        return ", ".join(COMMANDS) + "\n"


    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""

        if self.is_enabled(pchat_title):

            return ", ".join(BELLRINGER_HINT)
        return ""


    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""

        if pchat_title in self.config["chats"]:

            return UNIT_ID in self.config["chats"][pchat_title]
        return False


    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""

        return puser_name == self.config["master"]


    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
