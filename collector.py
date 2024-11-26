# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль выпрашивания пожертвований ;) """

# import string
from datetime import datetime
# from time import sleep
# from pathlib import Path
from random import randint

# import functions as func
# import constants as cn
import prototype

UNIT_ID = "collector"
WORK_HOURS: tuple = (12, 13, 14, 15, 16, 17, 18)
PROBABILITY: int = 16
CHANCE_VALUE: int = 8
DONATE_MESSAGE: str = ("\n\nНравится SoftIce? Поддержи проект! Пожертвуй 50 рублей на "
                       "содержание бота, это очень просто: "
                       "https://yoomoney.ru/to/41001510609674/50")


class CCollector(prototype.CPrototype):
    """Класс сборщика пожертвований"""

    def __init__(self, pconfig: dict):
        super().__init__()
        self.config: dict = pconfig

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Коллектор никакие команды не обрабатывает."""
        assert pchat_title is not None, \
            "Assert: [collector.can_process] Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [collector.can_process] Пропущен параметр <pmessage_text> !"
        return False

    def get_help(self, pchat_title: str):
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_hint(self, pchat_title: str):
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если коллектор разрешен на этом канале."""
        assert pchat_title is not None, \
            "Assert: [collector.is_enabled] Пропущен параметр <pchat_title> !"
        return UNIT_ID in self.config["chats"][pchat_title]

    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        return puser_name == self.config["master"]

    def collector(self, panswer: str) -> str:
        """Функция будет в определенные часы просить пожертвований."""

        # *** Время рабочее?
        just_now = datetime.now()
        if just_now.hour in WORK_HOURS:

            # *** Запросим случайное число
            chance: int = randint(1, PROBABILITY)
            #rint(f"chance: {chance} value {CHANCE_VALUE}")
            if chance == CHANCE_VALUE:

                # *** Сформируем ответ
                panswer = panswer + DONATE_MESSAGE

        return panswer

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
