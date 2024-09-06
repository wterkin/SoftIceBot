# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль для контроля над чатом."""
# from pathlib import Path
import functions as func
import prototype
import database as db

DATA_FOLDER: str = "supervisor"
DATABASE_NAME: str = "users.db"
STATUS_ACTIVE: int = 1
STATUS_INACTIVE: int = 0
# NEW_USER_RATING: int = 10
# STEP_VALUE: int = 20
# STEP_INCREMENT: int = 5
MINIMAL_TEXT_RATING: int = 10
MINIMAL_STICKER_RATING: int = 30
MINIMAL_PHOTO_RATING: int = 60
MINIMAL_AUDIO_RATING: int = 100
MINIMAL_VIDEO_RATING: int = 150
# KARMA_UPPER_LIMIT: int = 50
# ENABLED_IN_CHATS_KEY: str = "supervisor_chats"
UNIT_ID = "supervisor"
COMMANDS: list = ["svon", "svoff", "rt+", "rt-", "rt="]
PARAMETER_COUNT = "-c"
PARAMETER_FULL = "-f"


class CSupervisor(prototype.CPrototype):
    """ Класс смотрителя за чатом."""
    def __init__(self, pbot, pconfig, pdatabase):
        super().__init__()
        self.config = pconfig
        self.bot = pbot
        self.state = False
        self.admins: dict = {}
        self.create_admin_list()
        self.database: db.CDataBase = pdatabase

    def add_rights(self, puser_id: int, puser_name: str, pchat_id: int, pchat_title: str):
        """Добавляет в базу нового пользователя"""
        # ToDo: Вот тут нужно сначала получить внутренние ID юзера и чата!
        # rights = db.CRights(puser_id, pchat_id)
        # self.database.commit_changes(rights)
        # return rights.id

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        return self.is_enabled(pchat_title)

    def create_admin_list(self):
        """Создаёт двумерный список админов чатов."""

        for chat_name in self.config[ENABLED_IN_CHATS_KEY]:

            self.admins[chat_name] = []

    def delete_message(self, pmessage):
        """Удаляет сообщение пользователя."""
        # !!! self.bot.delete_message(chat_id=pmessage.chat.id, message_id=pmessage.message_id)
        # !!! print(f"> Сообщение пользователя {pmessage.from_user.username} в чате "
        # f"'{pmessage.chat.title}' удалено.")

    def get_chat_admin_list(self, pchat_id):
        """Возвращает список админов указанного чата."""
        return self.bot.get_chat_administrators(pchat_id)

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ""  # , ".join(HINT)

    def get_rights(self, pchat_id: int, puser_id: int):
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""
        # ToDo: Вот тут нужно сначала получить внутренние ID юзера и чата!
        # query = self.database.query_data(db.CRights)
        # query = query.filter_by(fchat_id=pchat_id, fuserid=puser_id)
        # rights = query.first()
        # if rights is not None:
        #
        #     return rights
        # return None
        pass

    def increment_karma(self, pmessage):
        """Увеличивает счётчик кармы на 1, если карма переполнится - увеличивает рейтинг."""
        rights: db.CRights = self.get_rights(pmessage.chat.id, pmessage.from_user.id)
        self.database.commit_changes(rights)

    def is_admin(self, pchat_id: int, puser_id: str):
        """Возвращает True, если пользователь является админом данного чата, иначе False."""

        # member = self.bot.get_chat_member(pchat_id, puser_id)
        # return member.is_chat_admin()
        # pass

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return UNIT_ID in self.config["chats"][pchat_title]
        # return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:

            return True, ""
        return False, f"У вас нет на это прав, {puser_title}."

    def reload(self):
        """ Заглушка. """

    def process_commands(self, pmessage):
        """Обрабатывает команды пользователя."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage.text)
        if self.can_process(pmessage.chat.title, pmessage.text):

            # *** Получим код команды
            command = func.get_command(word_list[0], COMMANDS)
            if command == 0:

                # *** Включить супервизор
                if self.is_master(pmessage.from_user.username, pmessage.from_user.first_name):

                    if not self.state:
                        self.state = True
                        print("* Супервизор активирован.")
                        answer = "Супервизор активирован."
            elif command == 1:
                # *** Выключить супервизор
                if self.is_master(pmessage.from_user.username, pmessage.from_user.first_name):

                    if self.state:
                        self.state = True
                        print("* Супервизор деактивирован.")
                        answer = "Супервизор деактивирован."
            elif command == 2:
                # *** Увеличить рейтинг на 1
                # reply_to_message
                pass
            elif command == 3:
                # *** Уменьшить рейтинг на 1
                pass
            elif command == 4:
                # *** Установить рейтинг
                pass
        return answer

    def supervisor(self, pmessage):
        """Контролирует поведение людей в чате."""
        answer: str = ""
        # # *** Если это ответ на сообщение..
        if pmessage.reply_to_message is not None:

            # from_part = pmessage.reply_to_message.json["from"]
            # *** ..получим ID пользователя, отправившего оригинальное сообщение
            # user_id = pmessage.reply_to_message.json["from"]["id"]
            # print(user_id)
            pass
        if pmessage.content_type == "text":

            answer = self.process_commands(pmessage)
        if self.state:

            if self.is_enabled(pmessage.chat.title):

                rights: db.CRights = self.get_rights(pmessage.chat.id, pmessage.from_user.id)
                if rights is not None:

                    if pmessage.content_type == "text":

                        if rights.fkarma < MINIMAL_TEXT_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                    elif pmessage.content_type == "sticker":

                        if rights.fkarma < MINIMAL_STICKER_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                    elif pmessage.content_type == "photo":

                        if rights.fkarma < MINIMAL_PHOTO_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                    elif pmessage.content_type in ["voice", "audio"]:

                        if rights.fkarma < MINIMAL_AUDIO_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                    elif pmessage.content_type in ["video", "video_note"]:

                        if rights.fkarma < MINIMAL_VIDEO_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                else:

                    name: str = pmessage.from_user.first_name + " "
                    if pmessage.from_user.last_name is not None:

                        name += pmessage.from_user.last_name
                        print(f"! {name}")
                    self.add_rights(pmessage.from_user.id, pmessage.chat.id)
        return answer
