# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль функций, связанных с БД."""
from pathlib import Path
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
# py lint: disable=C0301
# py lint: disable=line-too-long

DATABASE_VERSION: int = 1
DATABASE_NAME: str = "softice.db"
STATUS_ACTIVE: int = 1
STATUS_INACTIVE: int = 0

STATUSERID: str = "userid"
STATLETTERS: str = "letters"
STATWORDS: str = "words"
STATPHRASES: str = "phrases"
STATPICTURES: str = "pictures"
STATSTICKERS: str = "stickers"
STATAUDIOS: str = "audios"
STATVIDEOS: str = "videos"

MUTE_PENALTY = 1
BAN_PENALTY = 2
RUSSIAN_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"
WAITING_TIME: float = 0.1

convention = {
    "all_column_names": lambda constraint, table: "_".join([
        column.name for column in constraint.columns.values()
    ]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "cq": "cq__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__"
           "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s"
}

meta_data = MetaData(naming_convention=convention)
Base = declarative_base(metadata=meta_data)


class CAncestor(Base):
    """Класс-предок всех классов-моделей таблиц SQLAlchemy."""

    __abstract__ = True
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    fstatus = Column(Integer,
                     nullable=False,
                     )

    def __init__(self):
        """Конструктор."""

        self.fstatus = STATUS_ACTIVE

    def __repr__(self):

        return f"""ID:{self.id},
                   Status:{self.fstatus}"""

    def null(self):
        """Чтоб линтер был щаслиф."""


class CChat(CAncestor):
    """Класс справочника чатов."""

    __tablename__ = 'tbl_chats'
    fchatid = Column(Integer,
                     nullable=False,
                     unique=True,
                     index=True)
    fchatname = Column(String,
                       nullable=False,
                       )

    def __init__(self, pchat_id: int, pchat_name: str):
        """Конструктор"""

        super().__init__()
        self.fchatid = pchat_id
        self.fchatname = pchat_name

    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Chat ID:{self.fchatid}
                   Chat Name:{self.fchatname}"""


class CUser(CAncestor):
    """Класс модели таблицы справочника ID пользователей телеграмма."""

    __tablename__ = 'tbl_users'
    ftguserid = Column(Integer,
                       nullable=False,
                       unique=True,
                       index=True)
    fusername = Column(String,
                       nullable=True,
                       default="",
                       index=True
                       )

    def __init__(self, ptguserid: int, pusername: str = ""):
        """Конструктор"""

        super().__init__()
        self.ftguserid = ptguserid
        self.fusername = pusername

    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   TG user ID:{self.ftguserid},
                    User name:{self.fusername}"""

    def null(self):
        """Чтоб линтер был щаслив."""


class CStat(CAncestor):
    """Класс статистики."""

    __tablename__ = 'tbl_stat'
    fuserid = Column(Integer, ForeignKey(CUser.id))
    fchatid = Column(Integer, ForeignKey(CChat.id))
    fletters = Column(Integer, default=0)
    fwords = Column(Integer, default=0)
    fphrases = Column(Integer, default=0)
    fstickers = Column(Integer, default=0)
    fpictures = Column(Integer, default=0)
    faudios = Column(Integer, default=0)
    fvideos = Column(Integer, default=0)

    def __init__(self, puserid: int, pchatid: int, pdata_dict: dict):
        """Конструктор"""

        super().__init__()
        self.fuserid = puserid
        self.fchatid = pchatid
        self.set_all_fields(pdata_dict)

    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User id:{self.fuserid}
                   Letters:{self.fletters},
                   Words: {self.fwords},
                   Sentences: {self.fphrases},
                   Stickers: {self.fstickers},
                   Pictures: {self.fpictures},
                   Audios: {self.faudios},
                   Videos: {self.fvideos}"""

    def get_all_fields(self):
        """Возвращает словарь с данными класса."""
        fields_dict: dict = {STATUSERID: self.fuserid, STATLETTERS: self.fletters,
                             STATWORDS: self.fwords, STATPHRASES: self.fphrases,
                             STATPICTURES: self.fpictures, STATSTICKERS: self.fstickers,
                             STATAUDIOS: self.faudios, STATVIDEOS: self.fvideos}
        return fields_dict

    def set_all_fields(self, pdata_dict):
        """Присваивает полям записи данные из словаря."""
        self.fletters = pdata_dict[STATLETTERS]
        self.fwords = pdata_dict[STATWORDS]
        self.fphrases = pdata_dict[STATPHRASES]
        self.fstickers = pdata_dict[STATSTICKERS]
        self.fpictures = pdata_dict[STATPICTURES]
        self.faudios = pdata_dict[STATAUDIOS]
        self.fvideos = pdata_dict[STATVIDEOS]


class CRights(CAncestor):
    """Класс модели таблицы прав пользователей."""

    __tablename__ = 'tbl_rights'
    fuserid = Column(Integer, ForeignKey(CUser.id))
    fchatid = Column(Integer, ForeignKey(CChat.id))
    fkarma = Column(Integer, default=1000)
    fadmin = Column(Boolean, default=True)

    def __init__(self, puser_id: int, pchat_id: int):
        """Конструктор"""

        super().__init__()
        self.fuserid = puser_id
        self.fchatid = pchat_id

    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User ID:{self.fuserid}
                   Chat ID:{self.fchatid}
                   Karma:{self.fkarma}
                   Is admin:{self.fadmin}"""


class CSignal(CAncestor):
    """Класс таблицы сигнальщика."""

    __tablename__ = 'tbl_signal'
    fuserid = Column(Integer, ForeignKey(CUser.id))
    fword = Column(String)

    def __init__(self, puserid: int, pword: str):
        """Конструктор"""

        super().__init__()
        self.fuserid = puserid
        self.fword = pword


    def __repr__(self):

        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User id:{self.fuserid}
                   Word:{self.fword}"""


class CDataBase:
    """Класс."""

    def __init__(self, pconfig, pdata_path, pdatabase_name=DATABASE_NAME):
        """Конструктор класса."""
        self.application_folder = Path.cwd()
        self.config: dict = pconfig
        self.data_path: str = pdata_path
        self.session = None
        self.engine = None
        self.busy: bool = False
        self.database_name: str = pdatabase_name
        self.connect()


    def commit_changes(self, obj):
        """Сохраняет изменения в БД."""

        # *** Если база залочена - подождем.
        delayed: int = 0
        while self.busy:

            sleep(WAITING_TIME)
            delayed += 1
        # *** Теперь сами её залочим.
        self.busy = True
        # *** Сохраняем данные
        try:

            self.session.add(obj)
            self.session.commit()
            if delayed > 0:

                print(f"* Commit paused for {delayed//10} second.")
        except SQLAlchemyError:

            print("Ошибка!!!")
        finally:

            # *** Разлочим базу
            self.busy = False


    def connect(self):
        """Устанавливает соединение с БД."""

        result: bool = False
        # print(f"{self.data_path=} {self.database_name=}")
        try:
            alchemy_echo: bool = self.config["alchemy_echo"] == "1"
            self.engine = create_engine('sqlite:///' + self.data_path + self.database_name,
                                        echo=alchemy_echo,
                                        connect_args={'check_same_thread': False})
            session = sessionmaker()
            session.configure(bind=self.engine)
            self.session = session()
            Base.metadata.bind = self.engine
            result = True
        except exc.SQLAlchemyError:

            print("Ошибка подключения к БД!")
        return result


    def create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""

        Base.metadata.create_all(self.engine)


    def disconnect(self):

        """Разрывает соединение с БД."""
        self.session.close()
        self.engine.dispose()


    def exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""

        return Path(self.data_path + self.database_name).exists()


    def get_session(self):

        """Возвращает экземпляр session."""
        return self.session


    def query_data(self, cls):
        """Возвращает выборку заданнного класса."""

        # *** Если база залочена - подождем.
        while self.busy:

            sleep(WAITING_TIME)

        try:

            # *** Теперь сами её залочим.
            self.busy = True
            query = self.session.query(cls)
        finally:

            # *** Разлочим базу
            self.busy = False
        return query
