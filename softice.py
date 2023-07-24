#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
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

# *** Собственные модули
import functions as func
import database
import constants as cn
import babbler
import barman
import bellringer
import haijin
import librarian
import majordomo
import meteorolog
import moderator
import statistic
import stargazer
# import supervisor
import theolog

# *** Местоположение данных бота
ALLOWED_CHATS_KEY: str = "allowed_chats"
LINUX_DATA_FOLDER_KEY: str = "linux_data_folder"
LOGGING_KEY: str = "logging"
WINDOWS_DATA_FOLDER_KEY: str = "windows_data_folder"
TOKEN_KEY: str = "token"
CONFIG_FILE_NAME: str = "config.json"
BOT_NAME: str = "SoftIceBot"
COMMAND_SIGN: str = "!"
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие группы команд: \n"
EVENTS: list = ["text", "sticker", "photo", "audio", "video", "video_note", "voice"]
RUSSIAN_DATE_FORMAT: str = "%d.%m.%Y"
RUSSIAN_DATETIME_FORMAT: str = "%d.%m.%Y %H:%M:%S"

CONFIG_COMMANDS: list = ["конфиг", "config"]
EXIT_COMMANDS: list = ["прощай", "bye", "!!"]
HELP_COMMANDS: list = ["помощь", "help"]
RESTART_COMMAND: list = ["перезапуск", "restart", "22"]
NON_STOP: bool = True
POLL_INTERVAL: int = 0
CONTINUE_RUNNING: int = 0
QUIT_BY_DEMAND: int = 1
RESTART_BY_DEMAND: int = 2
BOT_STATUS: int = CONTINUE_RUNNING
RUNNING_FLAG: str = "running.flg"
SLEEP_BEFORE_EXIT_BY_ERROR: int = 10

# MCHAT_TITLE: str = "chat_title"
# MCHAT_ID: str = "chat_id"
# MCOMMAND: str = "command"
# MUSER_NAME: str = "user_name"
# MUSER_TITLE: str = "user_title"
# MTEXT: str = "text"
# MCAPTION: str = "caption"
# MDATE: str = "date"
# CONTENT_TYPE: str = "content_type"


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


def is_foreign_command(pcommand: str) -> bool:
    """Возвращает True, если в команде присутствует имя другого бота."""
    result: bool = False
    for bot in statistic.BOTS:

        result = bot in pcommand
        if result:

            break
    return result


# int: disable=too-many-instance-attributes # а что еще делать???
class CSoftIceBot:
    """Универсальный бот для Телеграмма."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.msg_rec: dict = {}
        # self.events: list = []
        self.event: dict = {}
        self.config: dict = {}
        self.load_config(CONFIG_FILE_NAME)
        # *** Нужно ли работать через прокси?
        if self.config["proxy"]:

            apihelper.proxy = {'https': self.config["proxy"]}
        # *** Создаём собственно бота.
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[TOKEN_KEY])
        self.bot_status: int = CONTINUE_RUNNING
        self.running_flag: str = os.getcwd() + "/" + RUNNING_FLAG
        if os.path.exists(self.running_flag):

            print("* Перезапуск после падения либо по требованию.")
            # logging.info("Перезапуск после падения либо по требованию.")
        else:

            with open(self.running_flag, 'tw', encoding='utf-8'):

                pass
        # *** Где у нас данные лежат?
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[WINDOWS_DATA_FOLDER_KEY]
        # *** Открываем БД
        self.database: database.CDataBase = database.CDataBase(self.config, self.data_path)
        if not self.database.exists():

            # *** А нету ещё БД, создавать треба.
            database.create()
        # *** Включаем логирование
        log_name: str = self.data_path+'softice.log'
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

        # *** Обработчик сообщений
        @self.robot.message_handler(content_types=EVENTS)
        def process_message(pmessage):

            answer: str
            # *** Вытаскиваем из сообщения нужные поля
            self.decode_message(pmessage)
            self.event = copy.deepcopy(self.msg_rec)
            # *** Проверим, легитимный ли этот чат
            answer = self.is_chat_legitimate(self.event).strip()
            if not answer:

                # *** Сообщение не протухло?
                if self.is_message_actual(self.event):

                    # *** Если это текстовое сообщение - обрабатываем в этой ветке.
                    if self.event[cn.MCONTENT_TYPE] == "text" and \
                            self.event[cn.MTEXT] is not None:

                        # *** Если сообщение адресовано другому боту - пропускаем
                        if not is_foreign_command(self.event[cn.MCOMMAND]):

                            # *** Если модератору что-то не понравилось...
                            answer = self.moderator.moderator(self.event).strip()
                            if not answer:

                                # ***  Боту дали команду?
                                if self.event[cn.MTEXT][0:1] == COMMAND_SIGN:

                                    # *** Это системная команда?
                                    if not self.process_command():

                                        # *** Нет. Ну и пусть модули разбираются....
                                        answer = self.process_modules(pmessage).strip()
                                else:

                                    # *** Нет. В этом чате статистик разрешен?
                                    if self.statistic.is_enabled(self.event[cn.MCHAT_TITLE]):

                                        # *** Проапдейтим базу статистика
                                        self.statistic.save_all_type_of_messages(self.event)

                                    # *** Болтуну есть что ответить?
                                    answer = self.babbler.talk(self.event).strip()
                    elif self.event[cn.MCONTENT_TYPE] in EVENTS:

                        self.statistic.save_all_type_of_messages(self.event)
            # *** Ответ имеется?
            if answer:

                self.send_answer(answer)

    def decode_message(self, pmessage):
        """Декодирует нужные поля сообщения в словарь."""
        if pmessage.text:

            text: str = pmessage.text.strip()
            self.msg_rec[cn.MCOMMAND] = text[1:]
            self.msg_rec[cn.MTEXT] = pmessage.text.strip()
        if pmessage.caption:

            self.msg_rec[cn.MCAPTION] = pmessage.caption.strip()
        self.msg_rec[cn.MCHAT_ID] = pmessage.chat.id
        self.msg_rec[cn.MCHAT_TITLE] = pmessage.chat.title.strip()
        self.msg_rec[cn.MUSER_ID] = pmessage.from_user.id
        if pmessage.from_user.username:

            self.msg_rec[cn.MUSER_NAME] = pmessage.from_user.username.strip()
        self.msg_rec[cn.MUSER_TITLE] = pmessage.from_user.first_name.strip()
        if pmessage.from_user.last_name:

            self.msg_rec[cn.MUSER_LASTNAME] = pmessage.from_user.last_name.strip()
        self.msg_rec[cn.MDATE] = pmessage.date
        self.msg_rec[cn.MCONTENT_TYPE] = pmessage.content_type
        self.msg_rec[cn.MMESSAGE_ID] = pmessage.message_id

    def is_chat_legitimate(self, pevent) -> str:
        """Проверяет, если ли этот чат в списке разрешенных."""
        answer: str = ""
        # *** Если это не приват...
        if pevent[cn.MCHAT_TITLE] is not None:

            # *** Если чата нет в списке разрешенных...
            if pevent[cn.MCHAT_TITLE] not in self.config[ALLOWED_CHATS_KEY]:

                # *** Бота привели на чужой канал. Выходим.
                self.robot.send_message(pevent[cn.MCHAT_ID],
                                        "Вашего чата нет в списке разрешённых. Чао!")
                self.robot.leave_chat(pevent[cn.MCHAT_ID])
                print("* Попытка нелегитимного использования "
                      f"бота в чате {pevent[cn.MCHAT_TITLE]}.")
                self.logger.warning("Попытка нелегитимного использования бота в чате %s.",
                                    pevent[cn.MCHAT_TITLE])
        else:
            answer = "Приваты с ботом запрещены."

        return answer

    def is_master(self) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        return self.event[cn.MUSER_NAME] == self.config["master"]

    def is_message_actual(self, pevent: dict) -> bool:
        """Проверяет, является ли сообщение актуальным."""
        date_time: datetime = datetime.fromtimestamp(pevent[cn.MDATE])
        return (datetime.now() - date_time).total_seconds() < 60

    def is_this_chat_enabled(self) -> bool:
        """Проверяет, находится ли данный чат в списке разрешенных."""
        return self.event[cn.MCHAT_TITLE] in self.config[ALLOWED_CHATS_KEY]

    def load_config(self, pconfig_name: str):
        """Загружает конфигурацию из JSON."""
        try:

            with open(pconfig_name, "r", encoding="utf-8") as json_file:

                self.config = json.load(json_file)
        except FileNotFoundError:

            print(f"* Файл конфигурации {pconfig_name} отсутствует.")
            self.logger.warning("* Файл конфигурации %s отсутствует.", pconfig_name)
            self.stop_working()

        except ValueError:

            print(f"* Ошибка в процессе парсинге файла конфигурации {pconfig_name}")
            self.logger.warning("* Ошибка в процессе парсинге файла конфигурации %s", pconfig_name)
            self.stop_working()

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

                self.robot.send_message(self.event[cn.MCHAT_ID], answer)
            result = True
        # *** Нет. Запросили рестарт?
        elif self.event[cn.MCOMMAND] in RESTART_COMMAND:

            self.restart()
            result = True
        return result

    def process_modules(self, pmessage):
        """Пытается обработать команду различными модулями."""
        # *** Проверим, не запросил ли пользователь что-то у бармена...
        rec: dict = copy.deepcopy(self.event)
        # do_not_screen: bool = False
        # *** Когда-нибудь я допишу супервайзера
        # !!! answer = self.supervisor.supervisor(pmessage)
        answer = self.moderator.moderator(rec)
        # print(f"*** moderator [{answer}]")
        if not answer:
            answer: str = self.barman.barman(rec[cn.MCHAT_TITLE],
                                             rec[cn.MUSER_NAME],
                                             rec[cn.MUSER_TITLE],
                                             rec[cn.MTEXT]).strip()
            # print(f"*** barmen [{answer}]")
        if not answer:

            # *** Или у звонаря
            answer = self.bellringer.bellringer(rec[cn.MCHAT_TITLE],
                                                rec[cn.MTEXT]).strip()
            # print(f"*** bellringer [{answer}]")
        if not answer:

            # *** ... или у хайдзина
            answer = self.haijin.haijin(rec[cn.MCHAT_TITLE],
                                        rec[cn.MUSER_NAME],
                                        rec[cn.MUSER_TITLE],
                                        rec[cn.MTEXT]).strip()
            # do_not_screen = True
            # print(f"*** haijin [{answer}]")
        if not answer:

            # *** ... или у библиотекаря...
            answer = self.librarian.librarian(rec[cn.MCHAT_TITLE],
                                              rec[cn.MUSER_NAME],
                                              rec[cn.MUSER_TITLE],
                                              rec[cn.MTEXT]).strip()
            # print(f"*** librarian [{answer}]")
        if not answer:

            # *** или у мажордома...
            answer = self.majordomo.majordomo(rec[cn.MCHAT_TITLE],
                                              rec[cn.MTEXT]).strip()
            # print(f"*** majordomo [{answer}]")
        if not answer:

            # *** ... или у метеоролога...
            answer = self.meteorolog.meteorolog(rec[cn.MCHAT_TITLE],
                                                rec[cn.MTEXT]).strip()
            # print(f"*** meteorolog [{answer}]")
        if not answer:

            # *** ... или у статистика...
            answer = self.statistic.statistic(rec[cn.MCHAT_ID],
                                              rec[cn.MCHAT_TITLE],
                                              rec[cn.MUSER_TITLE],
                                              rec[cn.MTEXT]).strip()
            # print(f"*** statistic [{answer}]")
        if not answer:

            # *** ... или у звездочёта...
            answer = self.stargazer.stargazer(rec[cn.MCHAT_TITLE],
                                              rec[cn.MTEXT]).strip()
            # print(f"*** stargazer [{answer}]")
        if not answer:

            # *** ... или у теолога...
            answer = self.theolog.theolog(rec[cn.MCHAT_TITLE],
                                          rec[cn.MTEXT]).strip()
            # print(f"*** theolog [{answer}]")
        if not answer:

            # *** ... может, у болтуна есть, что сказать?
            answer = self.babbler.babbler(rec).strip()
            # print(f"*** babbler [{answer}]")
        if not answer:

            # *** Незнакомая команда.
            print(f"* Запрошена неподдерживаемая команда {rec[cn.MTEXT]}.")
            self.logger.info("* Запрошена неподдерживаемая команда %s"
                             " в чате %s.", rec[cn.MTEXT], rec[cn.MCHAT_TITLE])
        return answer  # , do_not_screen

    def reload_config(self) -> bool:
        """Проверяет, не является ли поданная команда командой перезагрузки конфигурации."""
        # *** Такое запрашивать может только хозяин
        if self.is_master():

            self.robot.send_message(self.event[cn.MCHAT_ID], "Обновляю конфигурацию.")
            self.load_config(CONFIG_FILE_NAME)
            self.robot.send_message(self.event[cn.MCHAT_ID], "Конфигурация обновлена.")
            return True
        print(f"* Запрос на перезагрузку конфига "
              f"от нелегитимного лица {self.event[cn.MUSER_TITLE]}.")
        self.logger.warning("Запрос на перезагрузку конфига от нелегитимного лица %s.",
                            self.event[cn.MUSER_TITLE])
        self.robot.send_message(self.event[cn.MCHAT_ID],
                                f"У вас нет на это прав, {self.event[cn.MUSER_TITLE]}.")
        return False

    def send_answer(self, panswer):
        """Выбирает форматированный или неформатированный вывод"""
        answer: str
        # *** Выводим ответ
        if panswer[0:1] != cn.SCREENED:

            answer = func.screen_text(panswer)
        else:

            answer = panswer[1:]
        self.robot.send_message(self.event[cn.MCHAT_ID], answer,
                                parse_mode="MarkdownV2")

    def send_help(self) -> str:
        """Проверяет, не была ли запрошена подсказка."""
        # *** Собираем ответы модулей на запрос помощи
        answer: str = f"""\n{self.barman.get_hint(self.event[cn.MCHAT_TITLE])}
                          \n{self.bellringer.get_hint(self.event[cn.MCHAT_TITLE])}
                          \n{self.haijin.get_hint(self.event[cn.MCHAT_TITLE])}
                          \n{self.librarian.get_hint(self.event[cn.MCHAT_TITLE])}
                          \n{self.majordomo.get_hint(self.event[cn.MCHAT_TITLE])}
                          \n{self.meteorolog.get_hint(self.event[cn.MCHAT_TITLE])}
                          \n{self.statistic.get_hint(self.event[cn.MCHAT_TITLE])}
                          \n{self.stargazer.get_hint(self.event[cn.MCHAT_TITLE])}
                          \n{self.theolog.get_hint(self.event[cn.MCHAT_TITLE])}""".strip()
        # *** Если ответы есть, отвечаем на запрос
        if answer:

            return HELP_MESSAGE + answer
        return answer

    def stop_working(self):
        """Проверка, вдруг была команда выхода."""
        if self.is_master():

            self.robot.send_message(self.event[cn.MCHAT_ID], "Добби свободен!")
            os.remove(self.running_flag)
            raise CQuitByDemand()
        self.robot.send_message(self.event[cn.MCHAT_ID],
                                f"У вас нет на э"
                                f"то прав, {self.event[cn.MUSER_TITLE]}.")

    def restart(self):
        """Проверка, вдруг была команда рестарта."""
        if self.is_master():

            self.robot.send_message(self.event[cn.MCHAT_ID], "Щасвирнус.")
            raise CRestartByDemand()
        self.robot.send_message(self.event[cn.MCHAT_ID],
                                f"У вас нет на это прав, {self.event[cn.MUSER_TITLE]}.")

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
                sys.exit(2)
            except ReadTimeout:

                print("# Превышен интервал ожидания ответа. Выход.")
                self.logger.exception("Превышен интервал ожидания ответа. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
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

# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
# logging.basicConfig(filename='msg.log', filemode='w',
#   format='%(name)s - %(levelname)s - %(message)s')
# logging.debug('The debug message is displaying')
# logging.info('The info message is displaying')
# logging.warning('The warning message is displaying')
# logging.error('The error message is displaying')
# logging.critical('The critical message is displaying')
"""
            if not self.is_this_chat_enabled():

                # *** Если нет и это не приват...
                if self.msg_rec[cn.MCHAT_TITLE] is not None:

                    # *** Бота привели на чужой канал. Выходим.
                    self.robot.send_message(self.msg_rec[cn.MCHAT_ID],
                                            "Вашего чата нет в списке разрешённых. Чао!")
                    self.robot.leave_chat(self.msg_rec[cn.MCHAT_ID])
                    print("* Попытка нелегитимного использования "
                          f"бота в чате {self.msg_rec[cn.MCHAT_TITLE]}.")
                    self.logger.warning("Попытка нелегитимного использования бота в чате %s.",
                                        self.msg_rec[cn.MCHAT_TITLE])
                else:

                    answer = "Я в приватах не работаю."
            else:
"""
