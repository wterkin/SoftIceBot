# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль отладки."""

debug_state: bool = False  # True
# debug_state: bool = True


def dout(pmessage: str):
    """Выводит диагностические сообщения."""
    global debug_state
    if debug_state:

        print(pmessage)
