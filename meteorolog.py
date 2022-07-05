# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""

# from sys import path
import datetime
import subprocess
# import typing as tpn
import requests
import datetime as pdate

import functions as func
import prototype

# pylint: disable=wrong-import-position
# path.insert(0, "./")
# path.insert(0, "d:/Work/projects/")

# import owm
# os.system()

WEATHER_COMMANDS = ["погода", "пг", "weather", "wt"]
CHANNEL_LIST_KEY = "meteorolog_chats"  # X
ENABLED_IN_CHATS_KEY = "meteorolog_chats"
HINT = ["метео", "meteo"]
FIND_CITY_URL = "http://api.openweathermap.org/data/2.5/find"
FORECAST_WEATHER_URL = "http://api.openweathermap.org/data/2.5/forecast"


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
                                       'APPID': self.config["api_key"]})
            data = res.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
            print("city:", cities)
            city_id = data['list'][0]['id']
            print('city_id=', city_id)
        except Exception as ex:
            print("Exception (find):", ex)
            pass
        assert isinstance(city_id, int)
        return city_id

    def get_help(self) -> str:  # noqa
        """Пользователь запросил список команд."""
        command_list: str = ""
        for command in WEATHER_COMMANDS:
            command_list += command + ", "
        command_list = command_list[:-2]
        command_list += "\n"
        return command_list

    def get_weather(self, picon):
        result: str = ""
        if picon == "01d" or picon == "02d":

            result = "Ясно. 🌞"
        elif picon == "01n" or picon == "02n":

            result = "Ясно. 🌜"
        elif picon == "03d" or \
                picon == "03n" or \
                picon == "04d" or \
                picon == "04n":
            result = "Облачно. ☁"
        elif picon == "09d" or \
                picon == "09n" or \
                picon == "10d" or \
                picon == "10n":
            result = "Дождь. 🌧"
        if picon == "11d" or picon == "11n":
            result = "Гроза. 🌩"
        if picon == "13d" or picon == "13n":
            result = "Снег. ❄"
        if picon == "50d" or picon == "50n":
            result = "Туман.🌫"
        return result

    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [barman.get_hint] " \
            "No <pchat_title> parameter specified!"

        if self.is_enabled(pchat_title):
            return ", ".join(HINT)
        return ""

    def get_wind_direction(self, pdegree):  # noqa
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

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если метеоролог разрешен на этом канале."""

        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def meteorolog(self, pchat_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        message = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили меню.
            if word_list[0] in HINT:
                message = self.get_help()
            if word_list[0] in WEATHER_COMMANDS:

                if len(word_list) > 1:

                    city_name = word_list[1]
                    city_id = self.get_city_id(city_name)
                    message = self.request_forecast(city_id)
                else:

                    message = "Какую тебе еще погоду?"
        return message

    def reload(self):
        pass

    def request_forecast(self, pcity_id, plang: str = "ru"):
        """Запрос погоды на завтра."""
        message: str = ""
        now: datetime.datetime = datetime.datetime.now()
        tomorrow: datetime.datetime = now + pdate.timedelta(days=1)
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
        weather_line: str = ""
        try:

            res = requests.get(FORECAST_WEATHER_URL,
                               params={'id': pcity_id, 'units': 'metric',
                                       'lang': plang, 'APPID': self.config["api_key"]})
            data = res.json()
            for item in data['list']:

                # 1. Выбираем только завтрашние данные
                data_datetime: datetime.datetime = datetime.datetime.fromtimestamp(item['dt'])
                if data_datetime.date() == tomorrow.date():

                    main = item['main']
                    # *** Температура
                    if main["temp"] < min_temperature:
                        min_temperature = main["temp"]
                    if main["temp"] > max_temperature:
                        max_temperature = main["temp"]
                    # *** Давление
                    if main["pressure"] < min_pressure:
                        min_pressure = main["pressure"]
                    if main["pressure"] > max_pressure:
                        max_pressure = main["pressure"]
                    # *** Влажность
                    if main["humidity"] < min_humidity:
                        min_humidity = main["humidity"]
                    if main["humidity"] > max_humidity:
                        max_humidity = main["humidity"]
                    wind_speed = item["wind"]["speed"]
                    wind_angle = item["wind"]["deg"]
                    if wind_speed < min_wind_speed:
                        min_wind_speed = wind_speed
                        min_wind_angle = wind_angle
                    if wind_speed > max_wind_speed:
                        max_wind_speed = wind_speed
                        max_wind_angle = wind_angle
                    # print(item)
                    # break
                    # weather = item["weather"][0]
                    #print(icon[:-1])
                    icon = item["weather"][0]["icon"]

                    #print(icon[:-1])
                    #print(icon[0:2])

                    if icon[0:2] != "01":

                        icon = icon[0:2] + "d"
                    if icon[0:2] == "04":

                        icon = "03d"
                    elif icon[0:2] == "10":

                        icon = "09d"

                    if icon not in weather:

                        weather.append(icon)
            print(weather)
            for icon in weather:

                weather_line += self.get_weather(icon) + " "
            message = f"Темп.: {round(min_temperature)} - {round(max_temperature)} °C, " \
                      f" давл.: {round(min_pressure * 0.75)} - {round(max_pressure * 0.75)} мм.рт.ст., " \
                      f" влажн.: {round(min_humidity)} - {round(max_humidity)} %, " \
                      f" ветер: {round(min_wind_speed)} м/с {self.get_wind_direction(min_wind_angle)} " \
                      f"- {round(max_wind_speed)} м/c {self.get_wind_direction(max_wind_angle)}, " \
                      f" {weather_line}"


        except Exception as ex:

            print("Exception (forecast):", ex)
        return message
