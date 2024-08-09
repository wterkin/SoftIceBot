# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль тамагочи для бота."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Column, Integer, String, Boolean, DateTime 
from sqlalchemy.ext.declarative import declarative_base

import prototype
import functions as func
import constants as cn


TAMAGOTCHI_DATABASE: str = "tamagotchi.db"
HINT = ["tamagotchi", "тамагочи"]
RUS_COMMANDS = ["взять", "кормить", "миска", "лоток", "гладить"]
ENG_COMMANDS = ["get", "feed", "dish", "tray", "pet"]
UNIT_ID = "tamagotchi"
BOTS = ("TrueMafiaBot", "MafiaWarBot", "glagolitic_bot", "combot", "chgk_bot")
FOREIGN_BOTS = "foreign_bots"

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


class CTamagotchiModel(CAncestor):
    """Класс тамагочи"""

    __tablename__ = 'tbl_tamagotchi'
    fchatid = Column(Integer, nullable=False, unique=True, index=True)
    fchatname = Column(String, nullable=False)
    fuserid = Column(Integer, nullable=False, unique=True, index=True)
    fusername = Column(String, nullable=False)
    fname =  Column(String, default="Мурзик")
    fstate = Column(Boolean, default=True)
    fsatiety = Column(Integer, default=50)
    fhealth = Column(Integer, default=50)
    fmood = Column(Integer, default=50)
    fcoins = Column(Integer, default=1)    
    floyalty = Column(Integer, default=50)
    flastfeed = Column(DateTime(), default=dtime.now)
    flastplay = Column(DateTime(), default=dtime.now)                        
    ftraystate =  Column(Integer, default=0)
    flasttrayclean = Column(DateTime(), default=dtime.now)
    fdishstate =  Column(Integer, default=0)    
    flastdishcleanColumn = (DateTime(), default=dtime.now)

    def __init__(self, pchat_id: int, pchat_name: str, puser_id: int, puser_name: str):
        """Конструктор"""
        super().__init__()
        self.fchatid = pchat_id
        self.fchatname = pchat_name
        self.fuserid = puser_id
        self.fusername = puser_name

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Chat ID:{self.fchatid}
                   Chat Name:{self.fchatname}
                   User ID:{self.fuserid}
                   User Name:{self.fusername}
                   Name:{self.fname}
                   State:{self.fstate}
                   Satiety:{self.fsatiety}
                   Health:{self.fhealt}
                   Mood:{self.fmood}
                   Coins:{self.fcoins}
                   Loyalty:{self.floyalty}
                   Last Feed:{self.flastfeed}
                   Last Play:{self.flastplay}
                   Tray Staty:{self.ftraystate}
                   Last Tray Clean:{self.flasttrayclean}
                   Dish State:{self.fdishstate}
                   Last Dish Clean:{self.flastdishclean}
                   """

class CTamagotchi(prototype.CPrototype):
    """Класс статистика."""

    def __init__(self, pconfig: dict, pdata_path: str):
        super().__init__()
        self.locked: bool = False
        self.config: dict = pconfig
        self.engine = create_engine('sqlite:///' + self.data_path + TAMAGOTCHI_DATABASE,
                                    echo=1,
                                    connect_args={'check_same_thread': False})
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()
        Base.metadata.bind = self.engine
        
        if not Path(self.data_path + TAMAGOTCHI_DATABASE).exists():
            
            Base.metadata.create_all()
            
            

    def add_chat_to_base(self, ptg_chat_id: int, ptg_chat_title: str):
        """Добавляет новый чат в БД и возвращает его ID."""
        chat = db.CChat(ptg_chat_id, ptg_chat_title)
        self.database.commit_changes(chat)
        return chat.id

    def add_user_to_base(self, ptg_user_id: int, ptg_user_title: str):
        """Добавляет нового пользователя в БД и возвращает его ID."""

        user = db.CUser(ptg_user_id, ptg_user_title)
        self.database.commit_changes(user)
        return user.id

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду, иначе False."""
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            return word_list[0] in RUS_COMMANDS or 
                   word_list[0] in ENG_COMMANDS or
                   word_list[0] in HINT
        return False

    def get_chat_id(self, ptg_chat_id):
        """Если чат уже есть в базе, возвращает его ID, если нет - None."""
        # print(ptg_chat_id)
        query = self.database.query_data(db.CChat)
        # print(query)
        query = query.filter_by(fchatid=ptg_chat_id)
        # print(query)
        chat = query.first()
        # print(chat)
        if chat is not None:

            return chat.id
        return None

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        if self.is_enabled(pchat_title):

            command_list: str = ", ".join(RUS_COMMANDS)
            command_list += "\n, ".join(ENG_COMMANDS)"
            return command_list
        return ""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        if self.is_enabled(pchat_title):

            return ", ".join(HINT)
        return ""


    def get_user_id(self, ptg_user_id):
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""
        query = self.database.query_data(db.CUser)
        query = query.filter_by(ftguserid=ptg_user_id)
        user = query.first()
        if user is not None:

            return user.id
        return None


    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return UNIT_ID in self.config["chats"][pchat_title]
        # return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""


    def tamagotchi(self, pchat_id: int, pchat_title: str, puser_title, pmessage_text: str):
        """Обработчик команд."""
        command: int
        answer: str = ""
        order_by: int = 0
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            else:
                # *** Получим код команды
                command = func.get_command(word_list[0], COMMANDS)
                if command >= 0:

                    if len(word_list) > 1 and word_list[1].isdigit():

                        order_by = int(word_list[1])
                        if order_by < 1 or order_by > 6:

                            order_by = 1
                    if command in TOP_10_COMMAND:

                        answer = self.get_statistic(pchat_id, 10, order_by)
                    elif command in TOP_25_COMMAND:

                        answer = self.get_statistic(pchat_id, 25, order_by)
                    elif command in TOP_50_COMMAND:

                        answer = self.get_statistic(pchat_id, 50, order_by)
                    elif command in PERS_COMMAND:

                        answer = self.get_personal_information(pchat_id, puser_title)
        return answer
