#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль прототипа классов модулей бота."""

from abc import ABCMeta, abstractmethod  # , abstractproperty


class CPrototype:
    """Прототип классов модулей бота.. """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""

    @abstractmethod
    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""

    @abstractmethod
    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""

    @abstractmethod
    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""

    @abstractmethod
    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
