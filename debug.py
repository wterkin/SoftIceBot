# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль отладки."""

debug_state: bool = False  # True
# debug_state: bool = True


def dbg(pmessage: str):
    """Выводит диагностические сообщения."""
    global debug_state
    if debug_state:

        print(pmessage)
