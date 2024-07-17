 # -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""

import datetime as pdate
import requests

import functions as func
import prototype

WEATHER_COMMANDS: list = ["погода", "пг", "weather", "wt",
                          "прогноз", "пр", "forecast", "fr"]
ENABLED_IN_CHATS_KEY: str = "meteorolog_chats"
UNIT_ID: str = "meteorolog"
READ_TIMEOUT = 1
HINT: list = ["метео", "meteo"]
FIND_CITY_URL: str = 'http://api.openweathermap.org/data/2.5/find'
FORECAST_WEATHER_URL: str = 'http://api.openweathermap.org/data/2.5/forecast'
ICON_CONVERT: dict = {"01d": "Ясно. ☀️",
                      "02d": "Ясно. ☀️",
                      "01n": "Ясно. 🌜",
                      "02n": "Ясно. 🌜",
                      "03d": "Облачно. ☁",
                      "04d": "Облачно. ☁",
                      "03n": "Облачно. ☁",
                      "04n": "Облачно. ☁",
                      "09d": "Дождь. 🌧",
                      "10d": "Дождь. 🌧",
                      "09n": "Дождь. 🌧",
                      "10n": "Дождь. 🌧",
                      "11d": "Гроза. 🌩",
                      "11n": "Гроза. 🌩",
                      "13d": "Снег. ❄",
                      "13n": "Снег. ❄",
                      "50d": "Туман.🌫",
                      "50n": "Туман.🌫"}
RUSSIAN_DATE_FORMAT: str = "%d.%m.%Y"


def get_wind_direction(pdegree):
    """Возвращает направление ветра."""
    directions: list = ['сев. ', 'св', ' вост.', 'юв', 'юг ', 'юз', ' зап.', 'сз']
    result: str = ""
    for i in range(0, 8):

        step = 45.
        min_degree = i * step - 45 / 2.
        max_degree = i * step + 45 / 2.
        if i == 0 and pdegree > 360 - 45 / 2.:
            pdegree = pdegree - 360
        if min_degree <= pdegree <= max_degree:
            result = directions[i]
            break
    return result


def parse_weather(pdata, preq_date):
    """Парсит данные погоды и формирует строку погоды."""
    min_temperature: int = 100
    max_temperature: int = 0
    min_pressure: int = 10000
    max_pressure: int = 0
    min_humidity: int = 100
    max_humidity: int = 0
    min_wind_speed: int = 200
    max_wind_speed: int = 0
    min_wind_angle: int = 360
    max_wind_angle: int = 0
    weather: list = []

    for item in pdata['list']:

        # 1. Выбираем данные за заданную дату
        if pdate.datetime.fromtimestamp(item['dt']).date() == preq_date:

            # *** Температура
            min_temperature = min(item['main']["temp"], min_temperature)
            max_temperature = max(item['main']["temp"], max_temperature)
            # *** Давление
            min_pressure = min(item['main']["pressure"], min_pressure)
            max_pressure = max(item['main']["pressure"], max_pressure)
            # *** Влажность
            min_humidity = min(item['main']["humidity"], min_humidity)
            max_humidity = max(item['main']["humidity"], max_humidity)
            # *** Ветер
            wind_speed = item["wind"]["speed"]
            wind_angle = item["wind"]["deg"]
            if wind_speed < min_wind_speed:

                min_wind_speed = wind_speed
                min_wind_angle = wind_angle
            if wind_speed > max_wind_speed:

                max_wind_speed = wind_speed
                max_wind_angle = wind_angle
            # *** Иконка погоды
            icon = item["weather"][0]["icon"][0:2]
            # *** Если это не "ясно", то ночь не нужна
            icon = "01d" if icon in ["01", "02"] else icon + "d"
            if icon in ["04", "04d"]:

                # *** приводим всё к 3
                icon = "03d"
            # *** Если дождь
            elif icon == "10":

                # *** Приводим к 9
                icon = "09d"
            if icon not in weather:

                weather.append(icon)
    answer = f"Темп.: {round(min_temperature)} - {round(max_temperature)} °C, " \
             f" давл.: {round(min_pressure * 0.75)} - {round(max_pressure * 0.75)}" \
             f" мм.рт.ст., " \
             f" влажн.: {round(min_humidity)} - {round(max_humidity)} %, " \
             f" ветер: {round(min_wind_speed)} " \
             f"м/с {get_wind_direction(min_wind_angle)} " \
             f"- {round(max_wind_speed)} м/c {get_wind_direction(max_wind_angle)}, "
    for icon in weather:

        answer += ICON_CONVERT[icon] + " "
    return answer


class CMeteorolog(prototype.CPrototype):
    """Класс метеоролога."""

    def __init__(self, pconfig):
        super().__init__()
        self.config = pconfig

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если метеоролог может обработать эту команду"""

        if self.is_enabled(pchat_title):
            word_list: list = func.parse_input(pmessage_text)
            return word_list[0] in WEATHER_COMMANDS or word_list[0] in HINT
        return False

    # Проверка наличия в базе информации о нужном населенном пункте
    def get_city_id(self, pcity_name: str, plang: str = "ru"):
        """Возвращает ID города"""
        city_id: int = 0
        try:

            res = requests.get(FIND_CITY_URL,
                               params={'q': pcity_name, 'type': 'like',
                                       'units': 'metric', 'lang': plang,
                                       'APPID': self.config["api_key"]},
                               timeout=READ_TIMEOUT)
            data = res.json()
            if 'list' in data:

                if len(data['list']) > 0:

                    city_id = data['list'][0]['id']
        # except Exception as ex:
        except requests.TooManyRedirects as ex:
            print("Exception (find):", ex)
        except requests.Timeout as ex:
            print("Exception (find):", ex)
        except requests.HTTPError as ex:
            print("Exception (find):", ex)
        except requests.ConnectionError as ex:
            print("Exception (find):", ex)
        assert isinstance(city_id, int)
        return city_id

    def get_help(self, pchat_title: str) -> str:  # noqa
        """Пользователь запросил список команд."""
        if self.is_enabled(pchat_title):
            command_list: str = ", ".join(WEATHER_COMMANDS)
            command_list += "\n"
            return command_list
        return ""

    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [meteorolog.get_hint] " \
            "No <pchat_title> parameter specified!"

        if self.is_enabled(pchat_title):
            return ", ".join(HINT)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если метеоролог разрешен на этом канале."""
        if pchat_title in self.config["chats"]:

            return UNIT_ID in self.config["chats"][pchat_title]
        return False

    def meteorolog(self, pchat_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        # *** Метеоролог может обработать эту команду?
        if self.can_process(pchat_title, pmessage_text):

            # *** Запросили помощь?
            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
                return answer
            # *** Запросили погоду? А город указали?
            if len(word_list) > 1:

                # *** Получим ID города
                city_name = " ".join(word_list[1:])
                city_id = self.get_city_id(city_name)
                if city_id > 0:

                    # *** Указан существующий город, работаем.
                    now: pdate.datetime = pdate.datetime.now()
                    date_str: str = ""
                    weather_str: str = ""
                    # *** Прогноз на завтра?
                    if word_list[0] in ["прогноз", "пр", "forecast", "fr"]:

                        # *** Да, так и есть.
                        tomorrow: pdate.datetime = now + pdate.timedelta(days=1)
                        date_str = tomorrow.strftime(RUSSIAN_DATE_FORMAT)
                        weather_str = self.request_weather(city_id, tomorrow)

                    elif word_list[0] in ["погода", "пг", "weather", "wt"]:

                        # *** Нет, на сегодня. Еще не поздно?
                        if now.hour < 21:

                            # *** Вполне еще можно
                            date_str = now.strftime(RUSSIAN_DATE_FORMAT)
                            weather_str = self.request_weather(city_id, now)
                    # print(f"***** {weather_str}")
                    # *** Если еще не поздно, то выдадим погоду, иначе дадим знать юзеру
                    # answer = f"{city_name} : {date_str} : {weather_str}" if now.hour < 21 else
                    #    answer = "Поздно уже, какая тебе погода??!"
                    if now.hour < 21:

                        answer = f"{city_name} : {date_str} : {weather_str}"
                    else:

                        answer = "Уже слишком поздно, метеоролог уснул..."
                else:

                    answer = f"Нет данных о погоде для города {' '.join(word_list[1:]).strip()}"
            else:

                answer = "А в каком городе погода нужна?"
        return answer

    def reload(self):
        pass

    def request_weather(self, pcity_id, prequest_date: pdate.datetime, plang: str = "ru"):
        """Запрос погоды на завтра."""
        answer: str = ""
        try:

            # *** Запрашиваем информацию
            data = requests.get(FORECAST_WEATHER_URL,
                                params={'id': pcity_id, 'units': 'metric',
                                        'lang': plang, 'APPID': self.config["api_key"]},
                               timeout=READ_TIMEOUT).json()
            answer = parse_weather(data, prequest_date.date())

        except requests.TooManyRedirects as ex:
            print("Exception (find):", ex)
        except requests.Timeout as ex:
            print("Exception (find):", ex)
        except requests.HTTPError as ex:
            print("Exception (find):", ex)
        except requests.ConnectionError as ex:
            print("Exception (find):", ex)
        return answer
