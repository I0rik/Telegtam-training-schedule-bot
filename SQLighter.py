# -*- coding: utf-8 -*-

import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def select_all(self):
        """ Получаем всё расписание из БД, имя
            талицы передаётся аргументом в метод
            """
        with self.connection:
            query = 'SELECT date, time, subject, room, lecturer FROM training_schedule'
            self.cursor.execute(query)
            return self.cursor.fetchall()


    def get_shedule_on_day(self, date):
        """ Принимаем на вход дату, тащим из ДБ расписание на эту дату """
        with self.connection:
            query = "SELECT time, subject, room, lecturer FROM training_schedule WHERE date = date('{}')".format(date)
            self.cursor.execute(query)
            return self.cursor.fetchall()

    def get_dates(self):
        with self.connection:
            self.cursor.execute('SELECT date FROM training_schedule')
        return self.cursor.fetchall()


    def close(self):
        """ Закрываем соединение с БД """
        self.connection.close()
