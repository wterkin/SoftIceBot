#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
# Модуль игры в кошек
import prototype
import m_catgame
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import functions
import random
"""
Свойства кошки
1. Здоровье.
При охоте или битве уменьшается,
при кормлении или лечении увеличивается
2. Сила.
Увеличивается при игре и охоте. медленно.
3. Сытость.
Увеличивается при кормлении,
уменьшается при игре, охоте и в битве.
4. Настроение
Увеличивается при игре, ласке и кормлении, также после удачной охоты
Уменьшается после шлепка
5. Дисциплина
Увеличивается после шлепка
Уменьшается после нескольких поглаживаний (>2 подряд)
6. Внешность
Задаётся случайно при получении кота

Действия
1. Покормить
2. Погладить
3. Шлёпнуть
4. Отправить охотиться
5. Сделать кусь другому коту
6. Отвесить оплеуху другому коту
7. Устроить махач с другим котом

Инвентарь
1. Монеты
2. Игрушки
3. Корм

Добыча
Муха     -  5 м  3 урон
Кузнечик -  7 м  6 у
Мышонок  - 10 м  9 у
Лягушка  - 12 м 12 у
Мышь     - 15 м 15 у
Хомяк    - 17 м 18 у
Крыса    - 20 м 21 у
Белка    - 30 м 24 у
Хорёк    - 40 м 27 у
Ласка    - 50 м 30 у

Таблица кошек - привязывается к пользователю
+ Справочник пищи
+ Справочник игрушек

--Справочник лекарств
"""

CAT_GAME_DB: str = "cat_game.db"

CMD_REGISTRATION: int = 0
CMD_REFRESH: int = 1

COMMANDS: tuple = (("играть", "play"),
                   ("обновить", "refresh"),
                   )
ENABLED_IN_CHATS_KEY = "tomcat_chats"

HINTS: tuple = ("котоигра", "tomcat")

HEALTH_TERMINAL = 9
SATIETY_TERMINAL = 9
MOOD_TERMINAL = 9
DISCIPLINE_TERMINAL = 9
LOYALTY_TERMINAL = 9

TOMCAT_NAMES: tuple = ("Мурзик", "Барсик")
CAT_NAMES: tuple = ("Мурка", "Белка")
GENDERS: tuple = (0, 1)
COLORS: tuple = (("рыжая", "рыжий"),
                 ("чёрная", "чёрный"),
                 ("белая", "белый"),
                 ("бежевая", "бежевый"))
WOOLINESS: tuple = (("короткошёрстная", "короткошёрстный"),
                    ("средней шерстистости", "средней шерстистости"),
                    ("длинношёрстная", "длинношёрстный")
                   )
BREEDS: tuple = (("персидская", "персидский"),
                 ("сиамская", "сиамский"),
                 ("сибирская", "сибирский"),
                 ("мэйн-кун", "мэйн-кун"))

def recognize_command(pmessage_text: str):
    """Возвращает код переданной команды, если есть такая в списке."""
    cmd: str = pmessage_text.strip().lower()
    command_code: int = -1
    for index, command in enumerate(COMMANDS):

        if cmd in command:

            command_code = index
            break
    return command_code


class CTomCat(prototype.CPrototype):
    """Класс игры."""

    def __init__(self, pconfig: dict, pdata_path: str):
        super().__init__()
        self.config: dict = pconfig
        self.busy: bool = False
        self.data_path = pdata_path + 'tomcat/'
        self.engine = None
        self.session = None
        # self.database: database.CDataBase = database.CDataBase(self.config, self.data_path, CAT_GAME_DB)
        # print("** ", self.database.data_path)
        # print("** ", self.database.database_name)
        self.database_connect()
        if not self.database_exists():
            self.database_create()
        # self.session = self.database.get_session()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если бармен может обработать эту команду"""
        assert pchat_title is not None, \
            "Assert: [barman.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [barman.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = functions.parse_input(pmessage_text)
            for command in COMMANDS:

                found = word_list[0] in command
                if found:
                    break
        return found

    def create_cat(self, pdbuser_id):
        # fbreed = Column(String, nullable=False)
        cat_gender: int = random.choice(GENDERS)
        if cat_gender == 0:

            cat_name = random.choice(CAT_NAMES)
        else:

            cat_name = random.choice(TOMCAT_NAMES)
        cat_color = random.choice(COLORS)[cat_gender]
        cat_wooliness = random.choice(WOOLINESS)[cat_gender]
        cat_breed = random.choice(BREEDS)[cat_gender]
        # new_cat = m_catgame.CCat()
        pass

    def create_user(self, puser_id, puser_title):
        # *** Запишем пользователя в БД
        new_user = m_catgame.CGameUser(puser_id, puser_title)
        self.session.add(new_user)
        self.session.commit()
        # *** Выдадим ему игрушку базового уровня
        new_toy = m_catgame.CToyLink(new_user.id, 1)
        self.session.add(new_toy)
        self.session.commit()
        # *** Выдадим ему пару порций корма базового уровня
        new_feed = m_catgame.CFeedLink(new_user.id, 1)
        self.session.add(new_feed)
        new_feed = m_catgame.CFeedLink(new_user.id, 2)
        self.session.add(new_feed)
        self.session.commit()
        # *** Сгенерируем случайного кота
        # *** Предложим его пользователю

    def database_connect(self):
        """Устанавливает соединение с БД."""
        self.engine = create_engine('sqlite:///' + self.data_path + CAT_GAME_DB,
                                    echo=False,
                                    connect_args={'check_same_thread': False})
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        m_catgame.Base.metadata.bind = self.engine

    def database_create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        m_catgame.Base.metadata.create_all()
        self.session.commit()
        # *** Добыча
        prey = m_catgame.CPrey("Муха", 5, 3)
        self.session.add(prey)
        prey = m_catgame.CPrey("Кузнечик", 7, 6)
        self.session.add(prey)
        prey = m_catgame.CPrey("Мышонок", 10, 9)
        self.session.add(prey)
        prey = m_catgame.CPrey("Лягушка", 12, 12)
        self.session.add(prey)
        prey = m_catgame.CPrey("Хомяк", 17, 18)
        self.session.add(prey)
        prey = m_catgame.CPrey("Крыса", 20, 21)
        self.session.add(prey)
        prey = m_catgame.CPrey("Белка", 30, 24)
        self.session.add(prey)
        prey = m_catgame.CPrey("Хорёк", 40, 27)
        self.session.add(prey)
        prey = m_catgame.CPrey("Ласка", 50, 30)
        self.session.add(prey)
        self.session.commit()
        toy = m_catgame.CToy("Бантик на веревочке", 10, 3)
        self.session.add(toy)
        toy = m_catgame.CToy("Мячик", 20, 5)
        self.session.add(toy)
        toy = m_catgame.CToy("Заводная мышка", 50, 7)
        self.session.add(toy)
        toy = m_catgame.CToy("Лазерная указка", 100, 9)
        self.session.add(toy)
        self.session.commit()
        feed = m_catgame.CFeed("Молоко", 3, 1)
        self.session.add(feed)
        feed = m_catgame.CFeed("Рыба", 5, 2)
        self.session.add(feed)
        feed = m_catgame.CFeed("Вискас", 10, 3)
        self.session.add(feed)
        feed = m_catgame.CFeed("Китикэт", 15, 4)
        self.session.add(feed)
        feed = m_catgame.CFeed("Роял Канин", 25, 5)
        self.session.add(feed)
        self.session.commit()

    def database_disconnect(self):
        """Разрывает соединение с БД."""
        self.session.close()
        self.engine.dispose()

    def database_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        return Path(self.data_path + CAT_GAME_DB).exists()

    def get_help(self, pchat_title: str) -> str:
        """Пользователь запросил список команд."""
        assert pchat_title is not None, \
            "Assert: [barman.get_help] " \
            "No <pchat_title> parameter specified!"
        command_list: str = ""
        if self.is_enabled(pchat_title):

            for command in COMMANDS:
                command_list += ", ".join(command) + "\n"
        return command_list

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [barman.get_hint] " \
            "No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):
            return ", ".join(HINTS)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если бармен разрешен на этом канале."""
        assert pchat_title is not None, \
            "Assert: [barman.is_enabled] " \
            "No <pchat_title> parameter specified!"
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        pass

    def tomcat(self, pchat_title: str, puser_id: int, puser_title: str,
               pmessage_text: str):
        """Основная процедура модуля."""
        assert pchat_title is not None, \
            "Assert: [tomcat.tomcat] No <pchat_title> parameter specified!"
        assert puser_id is not None, \
            "Assert: [tomcat.tomcat] No <puser_id> parameter specified!"
        assert puser_title is not None, \
            "Assert: [tomcat.tomcat] No <puser_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [tomcat.tomcat] No <pmessage_text> parameter specified!"
        answer: str
        word_list: list = functions.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in HINTS:

                answer = "Игрок может использовать следующие команды: \n" + \
                         self.get_help(pchat_title)
            else:

                command: int = recognize_command(word_list[0])
                arguments = word_list[1:]
                if command == CMD_REGISTRATION:

                    self.create_user(puser_id, puser_title)
                    pass

        return answer
