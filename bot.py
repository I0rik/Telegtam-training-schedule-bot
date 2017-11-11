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
    result = '''/date - Показать расписание за выбранную дату.
/schedule - Показать расписание на семестр.
/subjects - Показать список предметов с ссылками на материалы.
/help - Справка.'''

    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['schedule'])
def schedule_print(message):
    """ Метод возвращает расписание на текущий семестр """
    result_message = ''

    db_worker = SQLighter(config.db_name)
    result = utils.sql_result_to_string(db_worker.select_all())
    result = result.split('\n\n')

    for row in result:
        row = row.split(', ')
        if len(row) > 1:
            result_message += "{}, `{}`, [{}]({}), `{}`, _{}_\n".format(
                row[0], row[1], row[2], row[3], row[4], row[5])

    bot.send_message(message.chat.id, result_message, parse_mode='Markdown')
    db_worker.close()


@bot.message_handler(commands=['subjects'])
def subjects_print(message):
    """ Метод возвращает список предметов """
    db_worker = SQLighter(config.db_name)
    result = utils.sql_result_to_string(db_worker.get_subjects())
    result = result.split(', ')
    result_message = ""

    for i in range(0, len(result) - 1, 3):
        result_message += "[{}]({}), _{}_;".format(
            result[i],
            result[i + 1],
            result[i + 2])

    bot.send_message(message.chat.id, result_message, parse_mode='Markdown')
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
    message_text = re.search(r'(в (чём|чем) смысл)|(ответ на вопрос жизни)',
                             message.text.lower())

    date = message.text
    db_worker = SQLighter(config.db_name)
    result = utils.sql_result_to_string(db_worker.get_schedule_on_day(date))

    if (message_text is not(None) and
            (message_text.group(0) == 'в чём смысл' or
             message_text.group(0) == 'в чем смысл' or
             message_text.group(0) == 'ответ на вопрос жизни')):
        bot.send_message(message.chat.id, '42', reply_markup=keyboard_hider)

    elif result == '':
        bot.send_message(
            message.chat.id,
            'Неизвестная команда, введите /help для помощи',
            reply_markup=keyboard_hider)

    else:
        """ Если получили из БД дату, режем результат
            на массив и формируем запрос
        """
        result_message = ''

        result = result.split('\n\n')

        for row in result:
            if len(row) > 1:
                row = row.split(', ')
                result_message += "`{}`, [{}]({}), `{}`, _{}_\n".format(
                    row[0], row[1], row[2], row[3], row[4])

        bot.send_message(
            message.chat.id,
            result_message,
            parse_mode='Markdown',
            reply_markup=keyboard_hider)


if __name__ == '__main__':
    bot.polling(none_stop=True)
