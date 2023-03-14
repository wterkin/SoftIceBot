# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль общих функций."""

BACKSLASH: str = "\\"
OUT_MSG_LOG_LEN = 60


def parse_input(pmessage_text: str) -> list:
    """Разбивает введённую строку на отдельные слова."""
    answer: str = ""
    if pmessage_text is not None:

        answer = pmessage_text[1:].strip().split(" ")
    return answer


def get_command(pword: str, pcommands : list) -> int:  # noqa
    """Распознает команду и возвращает её код, в случае неудачи - None."""
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
    """Загружает файл в список
    >>> load_from_file("data/bar/bar_test.txt")
    ['Test 1', 'Test 2', 'Test 3']
    >>> type(load_from_file("ABCDEF"))
    <class 'NoneType'>
    """
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
    # print(ptext)
    result_text: str = ptext.replace(".", f"{BACKSLASH}.")
    result_text = result_text.replace("-", f"{BACKSLASH}-")
    result_text = result_text.replace("!", f"{BACKSLASH}!")
    result_text = result_text.replace(")", f"{BACKSLASH})")
    result_text = result_text.replace("(", f"{BACKSLASH}(")
    result_text = result_text.replace("+", f"{BACKSLASH}+")
    result_text = result_text.replace("_", f"{BACKSLASH}_")
    result_text = result_text.replace("=", f"{BACKSLASH}=")
    # print(result_text)
    return result_text

