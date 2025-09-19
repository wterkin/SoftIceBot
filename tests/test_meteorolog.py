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
        
        data: list = []
        item: dict = {}
        item["dt"] = dtime.now.timestamp


