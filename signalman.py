# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov dog mail.ru
"""Модуль сигнальщика."""

import threading
import prototype

# ToDo: Хорошо бы каждому юзеру давать возможность зарегать область

MONITOR_URL: str = "https://dronemonitor.ru/"


"""
С помощью threading
Класс threading.Timer позволяет запустить функцию через указанный интервал. 
Конструктор: Timer(interval, function, args=None, kwargs=None). 
Параметры:
interval — интервал запуска функции;
function — функция, вызов которой нужно осуществить по таймеру;
args, kwargs — аргументы функции.
Методы:
timer.start() — запуск таймера;
timer.cancel() — останавливает работу таймера, если он ещё не сработал.
Ограничение: таймер вызывает указанную функцию через указанный интервал, но только один раз. Чтобы сделать работу повторяемой, нужно после срабатывания таймера создавать новый. 
"""

class CSignalMan(prototype.CPrototype):

    def __init__(self, pconfig: dict):

        
