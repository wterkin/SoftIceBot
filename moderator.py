# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль антимата для бота."""
import re
from pathlib import Path
import functions as func
import prototype
import constants as cn

RELOAD_BAD_WORDS: list = ["bwreload", "bwrl"]
HINT = ["адм", "adm"]
UNIT_ID = "moderator"

DATA_FOLDER: str = "moderator"
BAD_WORDS_FILE: str = "bad_words.txt"
CENSOR_PREFIX = r"\[\*\*"
CENSOR_POSTFIX = r"\*\*\]"
CENSORED: str = "*beep*"


def replace_bad_words(bad_word, text):
    """Заменяет мат в строке на безобидное слово."""

    words: list = text.split(" ")
    for wordindex, word in enumerate(words):

        if re.match(bad_word, word) is not None:

            words[wordindex] = CENSORED
    return " ".join(words)


class CModerator(prototype.CPrototype):
    """Класс модератора."""

    def __init__(self, pbot, pconfig, pdata_path: str):

        super().__init__()
        self.config = pconfig
        self.data_path: str = pdata_path + DATA_FOLDER + "/"
        self.bot = pbot
        self.bad_words: list = []
        self.reload()


    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""

        word_list: list = func.parse_input(pmessage_text)
        return self.is_enabled(pchat_title) and ((word_list[0] in RELOAD_BAD_WORDS)
                                                 or (word_list[0] in HINT))

    def check_bad_words_ex(self, pmessage: str) -> str:
        """Проверяет сообщение на наличие мата."""

        answer: str = ""
        detected: bool = False
        if pmessage is not None:

            text: str = pmessage.lower()
            for bad_word in self.bad_words:

                result: bool = True
                while result:

                    result = re.match(bad_word, text) is not None
                    if result:
                        

                        print("detected")
                        detected = True
                        text = replace_bad_words(bad_word, text)
            if detected:

                answer = text

        return answer


    def control_talking(self, prec):
        """Следит за матершинниками."""

        answer: str = ""
        source_text: str
        text: str

        if prec[cn.MCONTENT_TYPE] == "text":

            source_text = prec[cn.MTEXT]
        else:

            source_text = prec[cn.MCAPTION]
        if self.is_enabled(prec[cn.MCHAT_TITLE]):

            text = self.check_bad_words_ex(source_text)
            if text:

                self.bot.delete_message(chat_id=prec[cn.MCHAT_ID], message_id=prec[cn.MMESSAGE_ID])
                answer = prec[cn.MUSER_TITLE]
                if prec[cn.MUSER_LASTNAME]:

                    answer += " " + prec[cn.MUSER_LASTNAME]
                print(f"Пользователь {answer} матерился в чате {prec[cn.MCHAT_TITLE]}.")
                print(f"Он сказал: {source_text}")
                answer += f" хотел сказать \"{text}\""
        return answer


    def delete_message(self, pmessage):
        """Удаляет сообщение пользователя."""


    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""

        return ""


    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""

        return ", ".join(HINT)


    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""

        return UNIT_ID in self.config["chats"][pchat_title]


    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:

            return True, ""
        # *** Низзя
        print("> Moderator: Запрос на перезагрузку регэкспов "
              f"матерных выражений от нелегитимного лица {puser_title}.")
        return False, f"У вас нет на это прав, {puser_title}."


    def moderator(self, prec) -> str:
        """Процедура разбора запроса пользователя."""

        # *** Проверим, всё ли в порядке в чате
        answer: str = self.control_talking(prec)
        if not answer:

            if prec[cn.MTEXT] is not None:

                # *** Порядок. Возможно, запрошена команда. Мы ее умеем?
                if self.can_process(prec[cn.MCHAT_TITLE], prec[cn.MTEXT]):

                    # *** Да. Возможно, запросили перезагрузку.
                    word_list: list = func.parse_input(prec[cn.MTEXT])
                    if word_list[0] in RELOAD_BAD_WORDS:

                        # *** Пользователь хочет перезагрузить словарь мата.
                        can_reload, answer = self.is_master(prec[cn.MUSER_NAME],
                                                            prec[cn.MUSER_TITLE])
                        if can_reload:

                            self.reload()
                            answer = "Словарь мата обновлен"
                        else:

                            # *** ... но не тут-то было...
                            print(f"> Moderator: Запрос на перегрузку словаря мата от "
                                  f"нелегитимного лица {prec[cn.MUSER_TITLE]}.")
                            answer = (f"Извини, {prec[cn.MUSER_TITLE]}, "
                                      f"только {self.config['master_name']} может "
                                      "перегружать словарь мата!")
        return answer


    def reload(self):
        """Загружает словарь антимата."""

        # *** Собираем пути
        assert Path(self.data_path).is_dir(), f"{DATA_FOLDER} must be folder"
        data_path = Path(self.data_path) / BAD_WORDS_FILE
        self.bad_words.clear()
        self.bad_words = func.load_from_file(str(data_path))
        print(f"> Moderator успешно (пере)загрузил {len(self.bad_words)} "
              "регэкспов матерных выражений.")
