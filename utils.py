# -*- coding: utf-8 -*-

"""Создание клавиатуры для уточнения запроса боту"""

from telebot import types


def generate_markup(dates):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    for i in range(len(dates)):
        if i % 2 != 0:
            markup.row(dates[i - 1], dates[i])
        if (i == len(dates) - 1) and (len(dates) % 2 != 0):
            markup.row(dates[i])

    return markup


def sql_result_to_string(data):
    """Получаем результат SQL запроса и записываем его в одну строку"""
    result = ''
    for row in data:
        for elem in row:
            result = result + elem + ', '
        result += '\n\n'
    return result 