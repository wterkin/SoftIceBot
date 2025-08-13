# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль сигнальщика."""

import threading
import prototype
import database as db
import functions as func

# ToDo: Хорошо бы каждому юзеру давать возможность зарегать область

MONITOR_URL: str = "https://dronemonitor.ru/"


COMMANDS: list = ["monitor", "mon", "монитор", "мон", "forget", "forg", "забыть", "заб"]
HINT: list = ["сигнал", "signal"]
UNIT_ID: str = "signalman"
MONITOR: int = 0
FORGET: int = 4

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

    def __init__(self, pconfig: dict,  pdatabase: db.CDataBase):

        super().__init__()
        self.config: dict = pconfig
        self.database: db.CDataBase = pdatabase
        


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

                found = word_list[0] in HINT
        return found


    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""

        if self.is_enabled(pchat_title):

            return ", ".join(COMMANDS) + "\n"
        return "" 


    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""

        if self.is_enabled(pchat_title):

            return ", ".join(HINT)
        return ""


    def get_user_id(self, ptg_user_id):
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""

        query = self.database.query_data(db.CUser)
        query = query.filter_by(ftguserid=ptg_user_id)
        user = query.first()
        if user is not None:

            return user.id
        return None


    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""

        if pchat_title in self.config["chats"]:

            return UNIT_ID in self.config["chats"][pchat_title]
        return False


    def signalman(self, pchat_title: str, ptguser_id: int, pmessage_text: str):
        """Основная функция модуля."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили помощь.
            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            elif word_list[0] in COMMANDS[:4]:


                user_id: int = self.get_user_id(ptguser_id)
                # *** Регистрация
                if user_id > 0 and len(word_list) > 1:

    
                    self.register(user_id, word_list[1])
            elif word_list[0] in COMMANDS[FORGET:]:
                
               # *** Разрегистрация
                user_id: int = self.get_user_id(ptguser_id)
                if user_id > 0 and len(word_list) > 1:

    
                    self.forget(user_id, word_list[1])

               
    # def search_user_by_name(pusername: str):
    #    """Функция поиска ID пользователя по имени."""

            
    def monitor(self, puser_id: int, pword: str):
        """Функция регистрации темы пользователю."""

        signal = db.CSignalMan(puser_id, pword)
        self.database.commit_changes(signal)
        

    def reload(self, puser_id: int):
        """Вызывает перезагрузку внешних данных модуля."""
        
            
    def forget(puser_id: int, pword: str):
        """Функция разрегистрации темы пользователю."""

        query = self.database.query_data(db.CSignal)
        query = query.filter_by(puser_id)
        signal = query.first()
        signal.fstatus = db.STATUS_INACTIVE
        self.database.commit_changes(signal)
        
