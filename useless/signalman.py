# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль сигнальщика."""

import threading
import prototype
import database as db
import functions as func

# ToDo: Хорошо бы каждому юзеру давать возможность зарегать область

SITE_URL: str = "https://dronemonitor.ru/"


COMMANDS: list = ["monitor", "mon", "монитор", "мон", "forget", "forg", "забыть", "заб"]
HINT: list = ["сигнал", "signal"]
UNIT_ID: str = "signalman"
MONITOR: int = 0
FORGET: int = 4
MEMORIZE_MSG: str = "Запомнил."
FORGET_MSG: str = "Забыл."
USE_PROXY: bool = False
HTTP_PROXY: str = ""

if USE_PROXY:

    import urllib3 as ul
else:

    import urllib.request


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


    def download_page() -> list:
        """Скачивает страничку с сайта."""
        if USE_PROXY:

          proxy: object = ul.proxy_from_url(HTTP_PROXY, timeout=20.0)
          request: object = proxy.request("GET", SITE_URL)
          return request.data.decode('utf-8')
        else:

          return urllib.request.urlopen(SITE_URL).read().decode("UTF-8")
      

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
        answer: str = "Ошибка"
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили помощь.
            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            elif word_list[0] in COMMANDS[:4]:


                user_id: int = self.get_user_id(ptguser_id)
                # *** Регистрация
                if user_id > 0 and len(word_list) > 1:
    
                    if self.memorize(user_id, word_list[1]):

                      answer = MEMORIZE_MSG
            elif word_list[0] in COMMANDS[FORGET:]:
                
               # *** Разрегистрация
                user_id: int = self.get_user_id(ptguser_id)
                if user_id > 0 and len(word_list) > 1:

                    print(f"** 1 {user_id}")
                    if self.forget(user_id, word_list[1]):

                      answer = FORGET_MSG
        return answer       

            
    def memorize(self, puser_id: int, pword: str):
        """Функция регистрации темы пользователю."""
        result: bool = False
        try:

            signal = db.CSignal(puser_id, pword)
            self.database.commit_changes(signal)
            result = True
        except SQLAlchemyError as e:

            print(str(e.__dict__['orig']))
        return result
        

    def reload(self, puser_id: int):
        """Вызывает перезагрузку внешних данных модуля."""
        
            
    def forget(self, puser_id: int, pword: str) -> bool:
        """Функция разрегистрации темы пользователю."""

        result: bool = False
        try:

          print(f"** 21 {pword}")
          query = self.database.query_data(db.CSignal)
          query = query.filter_by(fuserid=puser_id)
          query = query.filter_by(fword=pword)
          query = query.filter_by(fstatus=db.STATUS_ACTIVE)
          signal = query.first()
          # print(f"** 22 {signal}")
          if signal is not None:

              
              signal.fstatus = db.STATUS_INACTIVE
              # print(f"** 22 {signal}")
              self.database.commit_changes(signal)
              result = True
        except SQLAlchemyError as e:

            print(str(e.__dict__['orig']))
        return result  
