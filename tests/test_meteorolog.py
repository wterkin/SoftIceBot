from unittest import TestCase
import json
import test_softice
import functions as func
import constants as cn
import meteorolog
import datetime as dtime

class CTestMeterolog(TestCase):

    def setUp(self) -> None:

        with open("unittest_config.json", "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        self.meteorolog: meteorolog.CMeteorolog = meteorolog.CMeteorolog(self.config)

    def test_get_wind_direction(self):
        
        self.assertEqual(meteorolog.get_wind_direction(180), meteorolog.DIRECTIONS[4]) # Юг
        self.assertEqual(meteorolog.get_wind_direction(270), meteorolog.DIRECTIONS[6]) # Запад

    
    def test_parse_weather(self):
        
        data: dict = {}
        temp_list: list = [10, 11, 12, 13]
        press_list: list = [700, 701, 702, 703]
        hum_list: list = [70, 80, 90, 100]
        wind_speed_list: list = [10, 20, 30, 40]
        wind_deg_list: list = [0, 45, 90, 180]
        data["list"] = []
        #now: dtime.datetime = dtime.now()
        now: dtime.datetime = dtime.datetime.now()
        
        for idx in range(0, len(temp_list)):
            
            item: dict = {}
            item["dt"] = now.timestamp()
            item['main']: dict = {}
            item['main']["temp"] = temp_list[idx]
            item['main']["pressure"] = press_list[idx]
            item['main']["humidity"] = hum_list[idx]
            item['wind']: dict = {}
            item["wind"]["speed"] = wind_speed_list[idx]
            item["wind"]["deg"] = wind_deg_list[idx]
            data["list"].append(item)
        result: str = "Темп.: 100 - 0 °C,  давл.: 7500 - 0 мм.рт.ст.,  влажн.: 100 - 0 %,  ветер: 200 м/с сев.  - 0 м/c сев. , "    
        self.assertEqual(meteorolog.parse_weather(data, now), result)
