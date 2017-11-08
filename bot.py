# -*- coding: utf-8 -*-

import config
import telebot
from telebot import types
from SQLighter import SQLighter
import utils
import re

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['help'])
def print_help_message(message):
    """ Метод возвращает описание и список команд """
    result = '''/date - Показать расписание за выбранную дату.\n/schedule - Показать расписание на семестр.\n/subjects - Показать список предметов с ссылками на материалы.\n/help - Справка.'''
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['schedule'])
def schedule_print(message):
    """ Метод возвращает расписание на текущий семестр """
    db_worker = SQLighter(config.db_name)
    result = utils.sql_result_to_string(db_worker.select_all())
    bot.send_message(message.chat.id, result, parse_mode='Markdown')
    db_worker.close()


@bot.message_handler(commands=['subjects'])
def schedule_print(message):
    """ Метод возвращает список предметов """
    db_worker = SQLighter(config.db_name)
    result = utils.sql_result_to_string(db_worker.get_subjects())
    bot.send_message(message.chat.id, result, parse_mode='Markdown')
    db_worker.close()


@bot.message_handler(commands=['date'])
def schedule_on_day_answer(message):
    """ Метод возвращает кастомную клавиатуру с датами """
    db_worker = SQLighter(config.db_name)
    dates_from_db = db_worker.get_dates()
    dates = []
    for date in dates_from_db:
        dates.append(date[0])
    markup = utils.generate_markup(dates)
    bot.send_message(message.chat.id, 'Выберите дату: ', reply_markup=markup)
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def schedule_on_day_print(message):
    """ Метод проверяет содержание введённого текста:
        если введена корректная дата - возвращает расписание на эту дату
        если ввод не корректный - выводится вспомогательное сообщение
        небольшая пасхалка если введён вопрос о смысле
    """
    keyboard_hider = types.ReplyKeyboardRemove()
    db_worker = SQLighter(config.db_name)
    date = message.text
    result = utils.sql_result_to_string(db_worker.get_schedule_on_day(date))

    message_text = re.search(r'(в (чём|чем) смысл)|(ответ на вопрос жизни)', message.text.lower())


    if message_text != None and (message_text.group(0) == 'в чём смысл' or message_text.group(0) == 'в чем смысл'
                                 or message_text.group(0) == 'ответ на вопрос жизни'):
        bot.send_message(message.chat.id, '42', reply_markup=keyboard_hider)
    elif result == '':
        bot.send_message(message.chat.id, 'Неизвестная команда, введите /help для помощи', reply_markup=keyboard_hider)
    else:
        bot.send_message(message.chat.id, result, parse_mode='Markdown', reply_markup=keyboard_hider)


if __name__ == '__main__':
    bot.polling(none_stop=True)
