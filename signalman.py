# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль сигнальщика."""

import threading
import prototype

# ToDo: Хорошо бы каждому юзеру давать возможность зарегать область

MONITOR_URL: str = "https://dronemonitor.ru/"


COMMANDS: list = ["рег", "reg", "разрег", "unreg"]
HINT: list = ["сигнал", "signal"]
UNIT_ID: str = "signalman"
REGISTRATION: int = 1
UNREGISTRATION: int = 3

"""
С помощью threading
Класс threading.Timer позволяет запустить функцию через указанный интервал. 
Конструктор: Timer(interval, function, args=None, kwargs=None). 
Параметры:
interval — интервал запуска функции;
function — функция, вызов которой нужно осуществить по таймеру;
args, kwargs — аргументы функции.
Методы:
timer.start() — запуск таймера;
timer.cancel() — останавливает работу таймера, если он ещё не сработал.
Ограничение: таймер вызывает указанную функцию через указанный интервал, но только один раз. Чтобы сделать работу повторяемой, нужно после срабатывания таймера создавать новый. 
"""

class CSignalMan(prototype.CPrototype):

    def __init__(self, pconfig: dict):


    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in COMMANDS:

                found = word_list[0] in command
                if found:

                    break
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


    def signalman(self, pchat_title: str, puser_name: str, pmessage_text: str):
        """Основная функция модуля."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили помощь.
            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            elif word_list[0] in [COMMANDS[0], COMMANDS[1]]:


                user_id: int = search_user_by_name(puser_name):
                # *** Регистрация
                if user_id > 0 and len(word_list) > 1:

    
                    self.register(user_id, word_list[1])
            elif word_list[0] in [COMMANDS[1], COMMANDS[2]]:
                
               # *** Разрегистрация
                user_id: int = search_user_by_name(puser_name):
                if user_id > 0 and len(word_list) > 1:

    
                    self.unregister(user_id, word_list[1])

               
    def search_user_by_name(pusername: str):
        """Функция поиска ID пользователя по имени."""

            
    def register(puser_id: int, pword: str):
        """Функция регистрации темы пользователю."""
        

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
        
            
    def unregister(puser_id: int, pword: str):
        """Функция разрегистрации темы пользователю."""
        
