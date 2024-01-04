# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль - цитатник хокку. 俳人"""

import functions as func
import prototype
import librarian
import constants as cn

# *** Команды для цитатника хокку
ASK_HOKKU_CMD: int = 0
ADD_HOKKU_CMD: int = 1
DEL_HOKKU_CMD: int = 2

RELOAD_BOOK: list = ["hokkureload", "hkrl"]
SAVE_BOOK: list = ["hokkusave", "hksv"]
HAIJIN_FOLDER: str = "haijin/"
HAIJIN_FILE_NAME: str = "hokku.txt"

HAIJIN_DESC: list = [" : получить случайное хокку, \n"
                     "хк, hk номер : с заданным номером \n"
                     "хк, hk строка : содержащее заданную строку",
                     " : добавить хокку в базу",
                     " : удалить хокку из базы"]

HAIJIN_COMMANDS: list = [["хк", "hk"],
                         ["хк+", "hk+"],
                         ["хк-", "hk-"]]

HINT = ["хокку", "hokku"]
UNIT_ID = "haijin"
BOLD: str = "*"
ITALIC: str = "_"
SPOILER: str = "||"
SLASH: str = "/"
LF: str = "\n"
SPACE: str = " "
LEFT_PARENTHESIS: str = "("
RIGHT_PARENTHESIS: str = ")"
LEFT_BRACKET: str = "["
RIGHT_BRACKET: str = "]"
AUTHOR_INDENT: str = "     "
DELIMITER: str = f"{func.BACKSLASH}|"


def get_command(pword: str) -> int:
    """Распознает команду и возвращает её код, в случае неудачи - None.
    """
    assert pword is not None, \
        "Assert: [haijin.get_command] " \
        "Пропущен параметр <pword> !"
    result: int = -1
    for command_idx, command in enumerate(HAIJIN_COMMANDS):

        if pword in command:

            result = command_idx
            break
    return result


class CHaijin(prototype.CPrototype):
    """Класс хайдзина."""

    def __init__(self, pconfig: dict, pdata_path: str):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + HAIJIN_FOLDER
        self.hokku: list = []
        self.reload()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если хайдзин может обработать эту команду."""
        assert pchat_title is not None, \
            "Assert: [haijin.can_process] " \
            "Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [haijin.can_process] " \
            "Пропущен параметр <pmessage_text> !"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in HAIJIN_COMMANDS:

                found = word_list[0] in command
                if found:

                    break

            if not found:

                found = word_list[0] in HINT
                if not found:

                    found = word_list[0] in RELOAD_BOOK
                    if not found:

                        found = word_list[0] in SAVE_BOOK
        return found

    def format_hokku(self, ptext: str) -> str:
        """Форматирует хокку так, как нам хочется."""
        # *** Вырежем номер
        result_text: str = ""
        if "???" not in ptext:

            if LEFT_BRACKET in ptext and RIGHT_BRACKET in ptext:

                left_par: int = ptext.index(LEFT_BRACKET)
                right_par: int = ptext.index(RIGHT_BRACKET)
                number: str = ptext[left_par + 1:right_par].strip()
                text: str = ptext[right_par + 1:]
                # *** Вырежем автора
                left_par = text.index(LEFT_PARENTHESIS)
                right_par = text.index(RIGHT_PARENTHESIS)
                author = text[left_par + 1:right_par].strip()
                text = text[:left_par]
                # *** Разобьём текст на строки
                text_list: list = text.split(SLASH)
                for line in text_list:

                    result_text += line.strip() + LF
                result_text = func.screen_text(result_text)
                result_text = f"{BOLD}{ITALIC}{result_text[:-1]}{ITALIC}{BOLD}{LF}" \
                              f"{AUTHOR_INDENT}{func.screen_text(author)} {SPOILER}" + \
                              f"{DELIMITER} {number} {DELIMITER} {len(self.hokku)} {SPOILER}"
            else:

                print(f"!!!!! {ptext} !!!!!!!!!!!!")
            return result_text
        return ptext

    def get_help(self, pchat_title: str) -> str:
        """Пользователь запросил список команд."""
        assert pchat_title is not None, \
            "Assert: [haijin.get_help] " \
            "Пропущен параметр <pchat_title> !"
        command_list: str = ""
        # ToDo: вот тут не выводится команда удаления
        if self.is_enabled(pchat_title):

            for idx, command in enumerate(HAIJIN_COMMANDS):

                if idx + 1 != len(HAIJIN_COMMANDS):

                    command_list += ", ".join(command) + HAIJIN_DESC[idx]
                    command_list += "\n"
        # print(f"***** {func.screen_text(command_list)} **********")

        return func.screen_text(command_list)

    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [haijin.get_hint] " \
            "Пропущен параметр <pchat_title> !"
        if self.is_enabled(pchat_title):

            return cn.SCREENED + func.screen_text(", ".join(HINT))
        return ""

    def haijin(self, pchat_title, puser_name: str, puser_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""
        assert pchat_title is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <pchat_title> !"
        assert puser_title is not None, \
            "Assert: [haijin.haijin] " \
            "Пропущен параметр <puser_title> !"
        answer: str = ""
        unformatted_answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили перезагрузку.
            if word_list[0] in RELOAD_BOOK:

                # *** Пользователь хочет перезагрузить книгу хокку
                can_reload, answer = self.is_master(puser_name, puser_title)
                if can_reload:

                    self.reload()
                    answer = "Книга загружена"
            elif word_list[0] in SAVE_BOOK:

                # *** Пользователь хочет сохранить книгу хокку
                can_reload, answer = self.is_master(puser_name, puser_title)
                if can_reload:

                    librarian.save_book(self.hokku, self.data_path + HAIJIN_FILE_NAME)
                    answer = "Книга сохранена"
            elif word_list[0] in HINT:

                answer = self.get_help(pchat_title)
                # print(f"[[[[{answer}]]]]")
            else:
                answer, unformatted_answer = self.process_command(word_list,
                                                                  puser_name,
                                                                  puser_title)
            if answer:

                if unformatted_answer:

                    print("> Haijin отвечает: ", unformatted_answer[:func.OUT_MSG_LOG_LEN])
                else:

                    print("> Haijin отвечает: ", answer[:func.OUT_MSG_LOG_LEN])
        if answer:

            answer = f"{cn.SCREENED}{answer}"
        return answer

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если библиотекарь разрешен на этом канале."""
        assert pchat_title is not None, \
            "Assert: [haijin.is_enabled] " \
            "Пропущен параметр <pchat_title> !"
        return UNIT_ID in self.config["chats"][pchat_title]
        # return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:

            return True, ""
        # *** Низзя
        return False, f"У вас нет на это прав, {puser_title}."

    def process_command(self, pcommand: list, puser_name: str, puser_title: str):
        """Обрабатывает пользовательские команды."""

        # *** Получим код команды
        answer: str = ""
        unformatted_answer: str = ""
        command: int = get_command(pcommand[0])
        if command >= 0:

            # *** Хокку запрашивали?
            if command == ASK_HOKKU_CMD:

                # *** Пользователь хочет хокку....
                answer = librarian.quote(self.hokku, pcommand)
                if answer:
                    unformatted_answer = answer
                    answer = self.format_hokku(unformatted_answer)
                    # print(unformatted_answer)
                    # print(answer)
                    # answer = ""
            elif command == ADD_HOKKU_CMD:

                # *** Пользователь хочет добавить хокку в книгу
                text: str = " ".join(pcommand[1:])
                if '(' not in text:

                    text += "(автор не  известен)"
                self.hokku.append(text)
                answer = f"Спасибо, {puser_title}, хокку добавлено под номером " \
                         f"{len(self.hokku)}"
            elif command == DEL_HOKKU_CMD:

                # *** Пользователь хочет удалить хокку из книги...
                if puser_name == self.config["master"]:

                    del self.hokku[int(pcommand[1]) - 1]
                    answer = f"Хокку {pcommand[1]} удалена."
                else:

                    # *** ... но не тут-то было...
                    print("> Haijin: Запрос на удаление хокку от "
                          f"нелегитимного лица {puser_title}.")
                    answer = (f"Извини, {puser_title}, "
                              f"только {self.config['master_name']} может удалять хокку")
        return answer, unformatted_answer

    def reload(self):
        """Перезагружает библиотеку."""

        self.hokku = librarian.load_book_from_file(self.data_path + HAIJIN_FILE_NAME)
        print(f"> Haijin успешно (пере)загрузил {len(self.hokku)} хокку.")
