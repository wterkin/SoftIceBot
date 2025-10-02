# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль общих функций."""
from datetime import datetime as dtime
import os

BACKSLASH: str = "\\"
OUT_MSG_LOG_LEN = 60


def parse_input(pmessage_text: str) -> list:
    """Разбивает введённую строку на отдельные слова."""
    answer: list = []
    if pmessage_text is not None:

        answer = pmessage_text[1:].strip().split(" ")
    return answer


def get_command(pword: str, pcommands : list) -> int:  # noqa
    """Распознает команду и возвращает её код, в случае неудачи  -1."""

    assert pword is not None, \
        "Assert: [function.get_command] " \
        "No <pword> parameter specified!"
    assert pcommands is not None, \
        "Assert: [function.get_command] " \
        "No <pcommands> parameter specified!"
    result: int = -1
    for command_idx, command in enumerate(pcommands):

        if pword in command:

            result = command_idx
            break

    return result


def load_from_file(pfile_name: str) -> list:
    """Загружает файл в список """
    content: list = []
    # *** откроем файл
    try:

        with open(pfile_name, encoding="utf8") as text_file:

            # *** читаем в список
            for line in text_file:

                if line:

                    content.append(line.strip())
    except FileNotFoundError:

        return content
    return content

def screen_text(ptext: str) -> str:
    """Экранирует текст перед выводом в телеграм."""
    result_text: str = ptext.replace(".", f"{BACKSLASH}.")
    result_text = result_text.replace("-", f"{BACKSLASH}-")
    result_text = result_text.replace("!", f"{BACKSLASH}!")
    result_text = result_text.replace(")", f"{BACKSLASH})")
    result_text = result_text.replace("(", f"{BACKSLASH}(")
    result_text = result_text.replace("+", f"{BACKSLASH}+")
    result_text = result_text.replace("_", f"{BACKSLASH}_")
    result_text = result_text.replace("=", f"{BACKSLASH}=")
    result_text = result_text.replace("*", f"{BACKSLASH}*")
    # print(f"****** {result_text=}")
    return result_text


def save_list(plist: list, pfile_name: str): # noqa
    """Сохраняет список строк в файл."""

    new_file_name: str = f"{pfile_name}_{dtime.now().strftime('%Y%m%d-%H%M%S')}"
    if os.path.exists(pfile_name):

        os.rename(pfile_name, new_file_name)
    with open(pfile_name, "w", encoding="utf8") as out_file:

        for line in plist:

            out_file.write(line + "\n")
