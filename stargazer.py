#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль прототипа классов модулей бота."""

from datetime import date, timedelta, datetime
import prototype
import functions as func

NEW_STYLE_OFFSET: int = 13
EASTER_CMD_INDEX: int = 0
DATE_CMD_INDEX: int = 1
DAY_CMD_INDEX: int = 2
COMMANDS: tuple = (("пасха", "easter"),
                   ("дата", "date"),
                   ("день", "day"))
HINTS: tuple = ("календарь", "кл", "calendar", "cl")
# ENABLED_IN_CHATS_KEY: str = "stargazer_chats"
UNIT_ID = "stargazer"
RUSSIAN_DATE_FORMAT = "%d.%m.%Y"
STARGAZER_FOLDER: str = "stargazer/"
LOW_MARGIN: int = 1899
HIGH_MARGIN: int = 2100
CHURCH_CALENDAR: str = "calendar.txt"
CIVILIAN_CALENDAR: str = "dates.txt"


def calculate_easter(pyear):
    """Вычисляет дату пасхи на заданный год."""
    first_value: int = (19 * (pyear % 19) + 15) % 30
    second_value: int = (2 * (pyear % 4) + 4 * (pyear % 7) + 6 * first_value + 6) % 7
    month: int
    day: int
    if (first_value + second_value) > 9:

        # *** Апрель
        month = 4
        day = (first_value + second_value) - 9 + NEW_STYLE_OFFSET
        if day > 30:
            month += 1
            day = day - 30
    else:

        # *** Март
        month = 3
        day = first_value + second_value + 22 + NEW_STYLE_OFFSET
        if day > 31:
            month += 1
            day = day - 31
    return date(pyear, month, day)


# def gather_day_and_month():
#     """Возвращает текущий день и месяц в формате DD/MM"""
#     now_date: date = date.today()
#     # day: int = now_date.day
#     # day_str = str(day)
#     day: str = f"{now_date.day:02}/{now_date.month:02}"
#     month: int = date.today().month
#     month_str = str(month)
#     if month < 10:
#         month_str = "0" + month_str
#     today: str = day_str + "/" + month_str
#     return today
#

class CStarGazer(prototype.CPrototype):
    """Класс модуля звездочёта."""

    def __init__(self, pconfig, pdata_path):
        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + STARGAZER_FOLDER

    def additional_info(self, pnow_date):
        """Возвращает дополнительные сведения об указанном дне."""
        answer: str = ""
        easter_date = calculate_easter(pnow_date.year)
        if easter_date > pnow_date:

            # *** Перед Пасхой
            if easter_date - pnow_date < timedelta(days=7):

                answer = "Страстная седмица."
            elif easter_date - pnow_date < timedelta(days=48):

                answer = "Великий пост"
            elif easter_date - pnow_date < timedelta(days=56):

                answer = "Сырная седмица"
            elif pnow_date < datetime(pnow_date.year, 1, 7):

                answer = "Рождественский пост"
            elif datetime(pnow_date.year, 1, 7) < pnow_date < datetime(pnow_date.year, 1, 18):

                answer = "Святки"
        # else:
        #
        #     # *** После Пасхи
        #     if (pnow_date > easter_date + timedelta(days=1)) and \
        #        (pnow_date < )

        return answer

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        assert pchat_title is not None, \
            "Assert: [stargazer.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [stargazer.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in COMMANDS:

                found = word_list[0] in command
                if not found:

                    found = word_list[0] in HINTS
                else:

                    break
        return found

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        assert pchat_title is not None, \
            "Assert: [stargazer.get_help] " \
            "No <pchat_title> parameter specified!"
        command_list: str = ""
        if self.is_enabled(pchat_title):

            for command in COMMANDS:
                command_list += ", ".join(command) + "\n"
        return command_list

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        assert pchat_title is not None, \
            "Assert: [stargazer.get_hint] " \
            "No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):
            return ", ".join(HINTS)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        assert pchat_title is not None, \
            "Assert: [stargazer.is_enabled] " \
            "No <pchat_title> parameter specified!"

        return UNIT_ID in self.config["chats"][pchat_title]
        # return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""

    def stargazer(self, pchat_title: str, pmessage_text: str) -> str:
        """Обработчик команд звездочёта."""
        assert pchat_title is not None, \
            "Assert: [stargazer.stargazer] No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [stargazer.stargazer] No <pmessage_text> parameter specified!"
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        year: int
        now_date: date = date.today()
        today: str
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили меню.
            if word_list[0] in HINTS:

                answer = self.get_help(pchat_title)
            # *** Запросили Пасху?
            elif word_list[0] in COMMANDS[EASTER_CMD_INDEX]:

                if len(word_list) > 1:

                    if word_list[1].isdigit():

                        year = int(word_list[1])
                    else:

                        year = 0
                else:

                    year = date.today().year
                if HIGH_MARGIN > year > LOW_MARGIN:

                    answer = calculate_easter(year).strftime(RUSSIAN_DATE_FORMAT)
                else:

                    answer = "Невозможно рассчитать Пасху на заданную дату."

            # *** Запросили гражданские праздники
            elif word_list[0] in COMMANDS[DATE_CMD_INDEX]:

                today = f"{now_date.day:02}/{now_date.month:02}"
                answer = self.search_in_calendar(CIVILIAN_CALENDAR, today)
            # *** Запросили церковные праздники
            elif word_list[0] in COMMANDS[DAY_CMD_INDEX]:

                today = f"{now_date.day:02}/{now_date.month:02}"
                answer = self.search_in_calendar(CHURCH_CALENDAR, today)
                answer += self.additional_info(now_date)
                # easter_date = calculate_easter(now_date.year)
                # if easter_date > today:
                #
                #     pass
                # else:
                #
                #     pass
        if answer:

            print(f"Stargazer answers: {answer[:func.OUT_MSG_LOG_LEN]}")
        return answer.strip()

    def search_in_calendar(self, pcalendar: str, ptoday: str):
        """Ищет заданную дату в заданном календаре."""
        calendar: list = func.load_from_file(self.data_path + pcalendar)
        answer: str = ""
        for item in calendar:

            if item[:5] == ptoday:

                answer += item[6:] + "\n"
        return answer[:-1:]
