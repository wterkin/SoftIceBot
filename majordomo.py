# from pathlib import Path
import random
import prototype
import functions as func

UNIT_ID = "majordomo"

COMMANDS: list = ["greet", "gr", "привет", "пт"]
MAJORDOMO_PATH: str = "majordomo/greetings.txt"


class CMajordomo(prototype.CPrototype):
    """Прототип классов модулей бота."""

    def __init__(self, pconfig: dict, pdata_path: str):
        super().__init__()
        self.config: dict = pconfig
        self.data_path: str = pdata_path + MAJORDOMO_PATH
        self.greetings: list = []
        self.reload()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in COMMANDS:

                found = word_list[0] in command
                if found:

                    break
        return found

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return self.get_hint(pchat_title)

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        if self.is_enabled(pchat_title):

            return ", ".join(COMMANDS)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        assert pchat_title is not None, \
            "Assert: [welcomer.is_enabled] Пропущен параметр <pchat_title> !"
        return UNIT_ID in self.config["chats"][pchat_title]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
        self.greetings = func.load_from_file(self.data_path)

    def majordomo(self, pchat_title, pmessage_text):
        """Главная функция модуля."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in COMMANDS:

                if len(word_list) > 1:

                    answer = random.choice(self.greetings) % word_list[1]
        return answer
