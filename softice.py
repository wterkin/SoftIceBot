#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Бот для Телеграмма"""

import copy
import os
from datetime import datetime
import time
import sys
from sys import platform
import json
import logging
import telebot
from telebot import apihelper
from requests import ReadTimeout, ConnectTimeout
import urllib3.exceptions
import pathlib

# *** Собственные модули
import functions as func
import database
import constants as cn
import babbler
import barman
import bellringer
import collector
import gambler
import haijin
import librarian
import majordomo
import meteorolog
import moderator
import statistic
import stargazer
# import supervisor
import theolog
import debug as dbg
# *** Местоположение данных бота

ALLOWED_CHATS_KEY: str = "allowed_chats"
LINUX_DATA_FOLDER_KEY: str = "linux_data_folder"
LOGGING_KEY: str = "logging"
WINDOWS_DATA_FOLDER_KEY: str = "windows_data_folder"
TOKEN_KEY: str = "token"

CONFIG_FILE_NAME: str = "config.json"
TRY_CONFIG_FILE_NAME: str = "try_config.json"
TRY_RUN_FLAG: str = "try.flg"
UNITTEST_CONFIG_NAME: str = "unittest_config.json"
UNITTEST_RUN_FLAG: str = "unittest.flg"
COMMAND_SIGN: str = "!"
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие группы команд: \n"
EVENTS: list = ["text", "sticker", "photo", "audio", "video", "video_note", "voice"]
RUSSIAN_DATE_FORMAT: str = "%d.%m.%Y"
RUSSIAN_DATETIME_FORMAT: str = "%d.%m.%Y %H:%M:%S"

CONFIG_COMMANDS: list = ["конфиг", "config"]
EXIT_COMMANDS: list = ["прощай", "bye", "!!", "носок"]
HELP_COMMANDS: list = ["помощь", "help"]
RESTART_COMMAND: list = ["перезапуск", "restart", "22"]
MUTE_COMMAND: list = ["молчи", "mute"]
UNMUTE_COMMAND: list = ["болтай", "talk"]
NON_STOP: bool = True
POLL_INTERVAL: int = 0
CONTINUE_RUNNING: int = 0
QUIT_BY_DEMAND: int = 1
RESTART_BY_DEMAND: int = 2
BOT_STATUS: int = CONTINUE_RUNNING
RUNNING_FLAG: str = "running.flg"
LEGAL_EXITING_FLAG: str = "exiting.flg"
SLEEP_BEFORE_EXIT_BY_ERROR: int = 10
ANSWERS_LOG: str = "logs/answers.log"
PRIVATE_IS_DISABLED_MSG: str = "Приваты с ботом запрещены."
NON_LEGITIMATE_CHAT_MSG: str = "Запрещено."
ANIMATIONS: tuple = (".gif", ".mp4", ".avi", ".mpg", ".wmv", ".flv")


class CQuitByDemand(Exception):
    """Исключение выхода."""

    def __init__(self):
        self.message: str = "* Выход по требованию."
        super().__init__(self.message)


class CRestartByDemand(Exception):
    """Исключение выхода."""

    def __init__(self):
        self.message: str = "* Перезапуск по требованию."
        super().__init__(self.message)


# message_id, date, chat, from_user=None, forward_from=None, forward_from_chat=None,
# forward_from_message_id=None, forward_date=None, reply_to_message=None, edit_date=None,
# text=None, entities=None, caption_entities=None, audio=None, document=None, game=None, photo=None,
# sticker=None, video=None, voice=None, video_note=None, new_chat_members=None, caption=None,
# contact=None, location=None, venue=None, left_chat_member=None, new_chat_title=None,
# new_chat_photo=None,
# delete_chat_photo=None, group_chat_created=None, supergroup_chat_created=None,
# channel_chat_created=None,
# migrate_to_chat_id=None, migrate_from_chat_id=None, pinned_message=None, invoice=None,
# successful_payment=None, forward_signature=None, author_signature=None, media_group_id=None,
# connected_website=None, animation=None, passport_data=None, poll=None, forward_sender_name=None,
# reply_markup=None, dice=None, via_bot=None, proximity_alert_triggered=None, sender_chat=None,
# video_chat_started=None, video_chat_ended=None, video_chat_participants_invited=None,
# message_auto_delete_timer_changed=None, video_chat_scheduled=None, is_automatic_forward=None,
# has_protected_content=None, web_app_data=None, is_topic_message=None, message_thread_id=None,
# forum_topic_created=None, forum_topic_closed=None, forum_topic_reopened=None,
# forum_topic_edited=None, general_forum_topic_hidden=None, general_forum_topic_unhidden=None,
# write_access_allowed=None, has_media_spoiler=None, user_shared=None,
# chat_shared=None, *, api_kwargs=None

# int: disable=too-many-instance-attributes # а что еще делать???
class CSoftIceBot:
    """Универсальный бот для Телеграмма."""

    def __init__(self):
        """Конструктор класса."""

        super().__init__()
        self.msg_rec: dict = {}
        self.event: dict = {}
        self.config: dict = {}
        self.config_is_correct: bool = False
        if os.path.exists(os.getcwd() + "/flags/" + UNITTEST_RUN_FLAG):

            self.config_is_correct = self.load_config(UNITTEST_CONFIG_NAME)
            print("** Using unittest config")
        elif os.path.exists(os.getcwd() + "/flags/" + TRY_RUN_FLAG):

            self.config_is_correct = self.load_config(TRY_CONFIG_FILE_NAME)
            print("** Using try config")
        else:

            self.config_is_correct = self.load_config(CONFIG_FILE_NAME)
            print("** Using work config")
        if self.config_is_correct:

            self.lock: bool = False
        else:

            sys.exit(0)
        self.silent: bool = False

	    # *** Нужно ли работать через прокси?
        if self.config["proxy"]:

            apihelper.proxy = {'https': self.config["proxy"]}
        if int(self.config["debugging"]) == 1:

            # global debug_state
            dbg.debug_state = True

        # *** Проверяем, не тестирование ли это
        self.testing: bool = False
        testing = self.config.get("testing")
        if testing is not None:

            self.testing = (int(testing) == 1)
	    # *** Создаём собственно бота.
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[TOKEN_KEY])
        self.bot_status: int = CONTINUE_RUNNING
        # *** Определим флаг работающего бота
        self.running_flag: str = os.getcwd() + "/flags/" + RUNNING_FLAG
        # *** Определим флаг выхода по требованию
        self.legal_exiting_flag: str = os.getcwd() + "/flags/" + LEGAL_EXITING_FLAG
        if os.path.exists(self.running_flag):

            print("* Перезапуск после падения либо по требованию.")
        else:
            # 91.240.87.48

            with open(self.running_flag, 'tw', encoding='utf-8'):

                # ***  оповещаем хозяина
                if not self.testing:

                    self.robot.send_message(self.config["master_id"], "Я внезапно упал. Вот несчастье.")
        # *** Где у нас данные лежат?
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[WINDOWS_DATA_FOLDER_KEY]
        # *** Открываем БД
        # print(self.data_path)
        self.database: database.CDataBase = database.CDataBase(self.config, self.data_path)
        if not self.database.exists():

            # *** А нету ещё БД, создавать нужно.
            self.database.create()
        # *** Включаем логирование
        log_name: str = './logs/softice.log'
        print(f"* Создаём файл журнала {log_name} с уровнем {self.config[LOGGING_KEY]}")
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        handler = logging.FileHandler(log_name)
        handler.setLevel(int(self.config[LOGGING_KEY]))
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # *** Поехали создавать объекты модулей =)
        self.babbler: babbler.CBabbler = babbler.CBabbler(self.config, self.data_path)
        self.barman: barman.CBarman = barman.CBarman(self.config, self.data_path)
        self.bellringer: bellringer.CBellRinger = bellringer.CBellRinger(self.config,
                                                                         self.data_path)
        self.collector: collector.CCollector = collector.CCollector(self.config)
        self.gambler: gambler.CGambler = gambler.CGambler(self.config)
        self.haijin: haijin.CHaijin = haijin.CHaijin(self.config, self.data_path)
        self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config, self.data_path)
        self.majordomo: majordomo.CMajordomo = majordomo.CMajordomo(self.config, self.data_path)
        self.meteorolog: meteorolog.CMeteorolog = meteorolog.CMeteorolog(self.config)
        self.moderator: moderator.CModerator = moderator.CModerator(self.robot, self.config,
                                                                    self.data_path)
        self.statistic: statistic.CStatistic = statistic.CStatistic(self.config, self.database)
        self.stargazer: stargazer.CStarGazer = stargazer.CStarGazer(self.config, self.data_path)
        self.theolog: theolog.CTheolog = theolog.CTheolog(self.config, self.data_path)
        # !!! self.supervisor: supervisor.CSupervisor =
        # supervisor.CSupervisor(self.robot, self.config,  self.database)
        print("*** Бот запущен.")
        # *** Обработчик сообщений
        @self.robot.message_handler(content_types=EVENTS)
        def process_message(pmessage):

            answer: str = ""
            file_name: str = ""
            # *** Вытаскиваем из сообщения нужные поля
            self.decode_message(pmessage)
            # if not self.msg_rec[cn.MPROCESSED]:
            # dbg.dout(f"si:pm:{self.msg_rec[cn.MCHAT_ID]}")
            if not self.lock:

                self.event = copy.deepcopy(self.msg_rec)
                # *** Проверим, легитимный ли этот чат
                # dbg.dout("si:pm:2")
                answer = self.is_chat_legitimate().strip()
                if not answer:

                    # *** Сообщение не протухло?
                    if self.is_message_actual():

                        # *** Если это текстовое сообщение - обрабатываем в этой ветке.
                        if self.event[cn.MCONTENT_TYPE] == "text" and \
                                self.event[cn.MTEXT] is not None:

                            # *** Если сообщение адресовано другому боту - пропускаем
                            if not self.is_foreign_command(self.event[cn.MCOMMAND]):

                                answer, file_name = self.process_modules()
                        self.statistic.save_all_type_of_messages(self.event)
                # *** Ответ имеется?
                if answer or file_name:

                    # *** Если не включён режим молчания...
                    if not self.silent:

                        self.send_answer(answer.strip(), file_name)




    def decode_message(self, pmessage):
        """Декодирует нужные поля сообщения в словарь."""

        # *** Сбрасываем флаг обработанности сообщения
        self.msg_rec[cn.MPROCESSED] = False
        # Если текст сообщения не пустой - обрабатываем
        if pmessage.text:

            text: str = pmessage.text.strip()
            self.msg_rec[cn.MCOMMAND] = text[1:]
            self.msg_rec[cn.MTEXT] = text

        else:

            self.msg_rec[cn.MCOMMAND] = ""
        if pmessage.caption:

            self.msg_rec[cn.MCAPTION] = pmessage.caption.strip()
        else:

            self.msg_rec[cn.MCAPTION] = ""
        # dbg.dout(f"*** si:dm {pmessage.chat}")
        self.msg_rec[cn.MCHAT_ID] = pmessage.chat.id
        if pmessage.chat.title:

            self.msg_rec[cn.MCHAT_TITLE] = pmessage.chat.title.strip()
        self.msg_rec[cn.MUSER_ID] = pmessage.from_user.id
        if pmessage.from_user.username:

            self.msg_rec[cn.MUSER_NAME] = pmessage.from_user.username.strip()
        else:

            self.msg_rec[cn.MUSER_NAME] = ""
        self.msg_rec[cn.MUSER_TITLE] = pmessage.from_user.first_name.strip()
        if pmessage.from_user.last_name:

            self.msg_rec[cn.MUSER_LASTNAME] = pmessage.from_user.last_name.strip()
        else:

            self.msg_rec[cn.MUSER_LASTNAME] = ""
        self.msg_rec[cn.MDATE] = pmessage.date
        self.msg_rec[cn.MCONTENT_TYPE] = pmessage.content_type
        self.msg_rec[cn.MMESSAGE_ID] = pmessage.message_id


    def is_chat_legitimate(self) -> str:
        """Проверяет, есть ли ли этот чат в списке разрешенных."""

        answer: str = ""
        # *** Если это не приват...
        chat_title: str = self.event.get(cn.MCHAT_TITLE)
        if chat_title is not None:

            # *** Если чата нет в списке разрешенных...
            if chat_title not in self.config[ALLOWED_CHATS_KEY]:

                # *** Бота привели на чужой канал. Выходим.
                self.say("Вашего чата нет в списке разрешённых. Чао!")
                self.leave_chat()
                print("* Попытка нелегитимного использования "
                      f"бота в чате {self.event[cn.MCHAT_TITLE]}.")
                self.logger.warning("Попытка нелегитимного использования бота в чате %s.",
                                    self.event[cn.MCHAT_TITLE])
                answer = NON_LEGITIMATE_CHAT_MSG
        else:
            answer = PRIVATE_IS_DISABLED_MSG

        return answer


    def is_foreign_command(self, pcommand: str) -> bool:
        """Возвращает True, если в команде присутствует имя другого бота."""

        result: bool = False
        # dbg.dout(f"sice:ifc: {}")
        for bot in self.config[statistic.FOREIGN_BOTS]:

            result = bot in pcommand
            if result:

                break
        return result


    def is_master(self) -> bool:
        """Проверяет, хозяин ли отдал команду."""

        if cn.MUSER_NAME in self.event:

            return self.event[cn.MUSER_NAME] == self.config["master"]
        return False


    def is_message_actual(self) -> bool:
        """Проверяет, является ли сообщение актуальным."""

        date_time: datetime = datetime.fromtimestamp(self.event[cn.MDATE])
        return (datetime.now() - date_time).total_seconds() < 60


    def leave_chat(self):
        """Покидает указанный чат."""

        if not self.testing:

            self.robot.leave_chat(self.event[cn.MCHAT_ID])


    def load_config(self, pconfig_name: str):
        """Загружает конфигурацию из JSON."""

        try:

            with open(pconfig_name, "r", encoding="utf-8") as json_file:

                self.config = json.load(json_file)
            return True
        except FileNotFoundError:

            print(f"* Файл конфигурации {pconfig_name} отсутствует.")
            return False
        except ValueError:

            print(f"* Ошибка в процессе парсинга файла конфигурации {pconfig_name}")
            return False


    def process_command(self) -> bool:
        """Обрабатывает системные команды"""

        result: bool = False
        # *** Это команда перезагрузки конфига?
        if self.event[cn.MCOMMAND] in CONFIG_COMMANDS:

            result = self.reload_config()
        # *** Нет. Запросили выход?
        elif self.event[cn.MCOMMAND] in EXIT_COMMANDS:

            self.stop_working()
            result = True
        # *** Опять нет. Запросили помощь?
        elif self.event[cn.MCOMMAND] in HELP_COMMANDS:

            answer: str = self.send_help()
            if answer:

                self.say(answer)
            result = True
        # *** Нет. Запросили рестарт?
        elif self.event[cn.MCOMMAND] in RESTART_COMMAND:

            self.restart()
            result = True
        elif self.event[cn.MCOMMAND] in MUTE_COMMAND:

            if self.is_master():

                #print("************ Ok")
                # dbg.dout("*** si:proccom: ********* Ok")
                self.silent = True
            else:

                # dbg.dout("*** si:proccom: !!!!!!!!!!!!!!!!!! No")
                self.say("Да щаз, так я и заткнулся.")
            result = True
        elif self.event[cn.MCOMMAND] in UNMUTE_COMMAND:

            if self.is_master():

                self.silent = False
            else:

                self.say("Как хозяин решит.")
            result = True
        return result


    def process_modules(self):
        """Пытается обработать команду различными модулями."""

        # *** Проверим, не запросил ли пользователь что-то у бармена...
        answer: str = ""
        file_name: str = ""
        # dbg.dout(f"*** si:procmod: 001 {self.event[cn.MTEXT]}")
        if not self.lock:

            self.lock = True
            rec: dict = copy.deepcopy(self.event)

            # ***  Боту дали команду?
            if self.event[cn.MTEXT][0:1] != COMMAND_SIGN:

                # dbg.dout("*** si:procmod: 002")
                # *** Нет, просто текст
                # *** Когда-нибудь я допишу супервайзера
                # !!! answer = self.supervisor.supervisor(pmessage)
                # *** Сначала пусть модератор поработает
                answer = self.moderator.control_talking(rec)
                if not answer:

                    # *** Болтуну есть что ответить?
                    if not self.silent:

                        answer, file_name = self.babbler.talk(self.event)
                # # *** Теперь очередь статистика...
                self.statistic.save_all_type_of_messages(self.event)
            else:

                # dbg.dout("*** si:procmod: 003")
                # *** Если команда не обработана обработчиком системных команд...
                if not self.process_command():

                    # dbg.dout("*** si:procmod: 004")
                    # *** Сначала модератор
                    answer = self.moderator.moderator(rec)
                    # dbg.dout(f"*** si:procmod:moderator [{answer}]")
                    if not answer:

                        # *** ... потом бармен
                        answer: str = self.barman.barman(rec[cn.MCHAT_TITLE],
                                                         rec[cn.MUSER_NAME],
                                                         rec[cn.MUSER_TITLE],
                                                         rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:barmen [{answer}]")
                    if not answer:


                        # *** ... потом звонарь
                        answer = self.bellringer.bellringer(rec[cn.MCHAT_TITLE],
                                                            rec[cn.MUSER_NAME],
                                                            rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:bellringer [{answer}]")
                    if not answer:

                        # *** ... потом игрок
                        answer = self.gambler.gambler(rec[cn.MCHAT_TITLE],
                                                      rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:gambler [{answer}]")
                    if not answer:

                        # *** ... потом хайдзин
                        answer = self.haijin.haijin(rec[cn.MCHAT_TITLE],
                                                    rec[cn.MUSER_NAME],
                                                    rec[cn.MUSER_TITLE],
                                                    rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:haijin [{answer}]")
                    if not answer:

                        # *** ... потом библиотекарь
                        answer = self.librarian.librarian(rec[cn.MCHAT_TITLE],
                                                          rec[cn.MUSER_NAME],
                                                          rec[cn.MUSER_TITLE],
                                                          rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:librarian [{answer}]")
                    if not answer:

                        # *** ... потом мажордом
                        answer = self.majordomo.majordomo(rec[cn.MCHAT_TITLE],
                                                          rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:majordomo [{answer}]")
                    if not answer:

                        # *** ... потом метеоролог
                        answer = self.meteorolog.meteorolog(rec[cn.MCHAT_TITLE],
                                                            rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:meteorolog [{answer}]")
                    if not answer:

                        # *** ... потом статистик
                        answer = self.statistic.statistic(rec[cn.MCHAT_ID],
                                                          rec[cn.MCHAT_TITLE],
                                                          rec[cn.MUSER_TITLE],
                                                          rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:statistic [{answer}]")
                    if not answer:

                        # *** ... потом звездочёт
                        answer = self.stargazer.stargazer(rec[cn.MCHAT_TITLE],
                                                          rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:stargazer [{answer}]")
                    if not answer:

                        # *** ... потом теолог
                        answer = self.theolog.theolog(rec[cn.MCHAT_TITLE],
                                                      rec[cn.MTEXT]).strip()
                        dbg.dout(f"*** si:procmod:theolog [{answer}]")
                    if not answer:

                        # *** ... потом болтун
                        if not self.silent:

                            answer = self.babbler.babbler(rec).strip()
                            dbg.dout(f"*** si:procmod:babbler [{answer}]")
                    if not answer:

                        # *** Незнакомая команда.
                        dbg.dout(f"*** si:procmod: Запрошена неподдерживаемая команда {rec[cn.MTEXT]}.")
                        self.logger.info("* Запрошена неподдерживаемая команда %s"
                                         " в чате %s.", rec[cn.MTEXT], rec[cn.MCHAT_TITLE])
            answer = answer.strip()
            if answer:

                if self.collector.is_enabled(rec[cn.MCHAT_TITLE]):

                    answer = self.collector.collector(answer)
            self.lock = False
        return answer, file_name


    def reload_config(self) -> bool:
        """Проверяет, не является ли поданная команда командой перезагрузки конфигурации."""

        # *** Такое запрашивать может только хозяин
        if self.is_master():

            self.say("Обновляю конфигурацию.")
            self.load_config(CONFIG_FILE_NAME)
            self.say("Конфигурация обновлена.")
            return True
        print(f"* Запрос на перезагрузку конфига "
              f"от нелегитимного лица {self.event[cn.MUSER_TITLE]}.")
        self.logger.warning("Запрос на перезагрузку конфига от нелегитимного лица %s.",
                            self.event[cn.MUSER_TITLE])
        self.say(f"У вас нет на это прав, {self.event[cn.MUSER_TITLE]}.")
        return False


    def say(self, pmessage: str, pparse_mode: str=""):
        """Выводит сообщение в указанный чат."""

        if not self.testing:

            self.robot.send_message(self.event[cn.MCHAT_ID], pmessage, pparse_mode)

    def send_answer(self, panswer, pfile_name: str = ""):
        """Выбирает форматированный или неформатированный вывод"""

        answer: str
        # *** Выводим ответ
        if panswer[0:1] != cn.SCREENED:

            answer = func.screen_text(panswer)
        else:

            answer = panswer[1:]
        if pfile_name:

            # dbg.dout(f"*** sice:sndans: {pfile_name}")
            self.send_img(pfile_name, self.event[cn.MCHAT_ID], answer)
        self.say(answer, pparse_mode="MarkdownV2")


    def send_img(self, pfilename: str, pchat_id: int, panswer: str):
        """Отправляет в чат картинку."""

        with open(pfilename, 'rb') as image:

            # dbg.dout(f"*** sice:sndgif: {pchat_id}, {panswer}")
            extension = pathlib.Path(pfilename).suffix
            if extension in ANIMATIONS:

                self.robot.send_animation(pchat_id, image, None, panswer)
            else:

                self.robot.send_photo(pchat_id, image)


    def send_help(self) -> str:
        """Проверяет, не была ли запрошена подсказка."""

        # *** Собираем ответы модулей на запрос помощи
        answer: str = ""
        result: str = self.barman.get_hint(self.event[cn.MCHAT_TITLE])
        if result:

            answer += result + "\n"
        result = self.bellringer.get_hint(self.event[cn.MCHAT_TITLE])
        if result:

            answer += result + "\n"
        result = self.haijin.get_hint(self.event[cn.MCHAT_TITLE])[1:]
        if result:

            answer += result + "\n"
        result = self.librarian.get_hint(self.event[cn.MCHAT_TITLE])
        if result:

            answer += result + "\n"
        result = self.majordomo.get_hint(self.event[cn.MCHAT_TITLE])
        if result:

            answer += result + "\n"
        result = self.meteorolog.get_hint(self.event[cn.MCHAT_TITLE])
        if result:

            answer += result + "\n"
        result = self.statistic.get_hint(self.event[cn.MCHAT_TITLE])
        if result:

            answer += result + "\n"
        result = self.stargazer.get_hint(self.event[cn.MCHAT_TITLE])
        if result:

            answer += result + "\n"
        result = self.theolog.get_hint(self.event[cn.MCHAT_TITLE])
        if result:

            answer += result + "\n"
        # *** Если ответы есть, отвечаем на запрос
        if answer:

            return HELP_MESSAGE + answer
        return answer


    def stop_working(self):
        """Проверка, вдруг была команда выхода."""

        if self.is_master():

            if hasattr(self, 'robot'):

                self.say("Добби свободен!")
            with open(self.legal_exiting_flag, 'tw', encoding='utf-8'):

                pass
            os.remove(self.running_flag)
            raise CQuitByDemand()
        self.say(f"У вас нет на это прав, {self.event[cn.MUSER_TITLE]}.")


    def restart(self):
        """Проверка, вдруг была команда рестарта."""

        if self.is_master():

            self.say("Щасвирнус.")
            raise CRestartByDemand()
        self.say(f"У вас нет на это прав, {self.event[cn.MUSER_TITLE]}.")


    def poll_forever(self):
        """Функция опроса ботом телеграмма."""

        while self.bot_status == CONTINUE_RUNNING:

            try:

                self.robot.polling(interval=POLL_INTERVAL)
            except CQuitByDemand as exception:

                self.logger.exception(exception.message)
                self.bot_status = QUIT_BY_DEMAND
                self.robot.stop_polling()
                sys.exit(0)
            except CRestartByDemand as exception:

                self.logger.exception(exception.message)
                self.bot_status = RESTART_BY_DEMAND
                self.robot.stop_polling()
                sys.exit(1)
            except ConnectionError:

                print("# Соединение прервано. Выход.")
                self.logger.exception("Соединение прервано. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
                self.robot.stop_polling()
                sys.exit(2)
            except ReadTimeout:

                print("# Превышен интервал ожидания ответа. Выход.")
                self.logger.exception("Превышен интервал ожидания ответа. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
                self.robot.stop_polling()
                sys.exit(3)
            except telebot.apihelper.ApiTelegramException:

                print("# Telegram отказал в соединении. Выход.")
                self.logger.exception("Telegram отказал в соединении. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR*2)
                sys.exit(4)
            except urllib3.exceptions.MaxRetryError:

                print("# Слишком много попыток соединения. Выход.")
                self.logger.exception("Слишком много попыток соединения. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR*2)
                sys.exit(5)
            except ConnectTimeout:

                print("# Превышен интервал времени для соединения. Выход.")
                self.logger.exception("Превышен интервал времени для соединения. Выход.",
                                      exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
                sys.exit(6)
            except urllib3.exceptions.ProtocolError:

                print("# Соединение разорвано. Выход.")
                self.logger.exception("Соединение разорвано. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
                sys.exit(7)


if __name__ == "__main__":

    print(f"* SoftIce (пере)запущен {datetime.now().strftime(RUSSIAN_DATETIME_FORMAT)}")
    SofticeBot: CSoftIceBot = CSoftIceBot()
    SofticeBot.logger.info("SoftIce (пере)запущен %s",
                           datetime.now().strftime(RUSSIAN_DATETIME_FORMAT))
    SofticeBot.poll_forever()
