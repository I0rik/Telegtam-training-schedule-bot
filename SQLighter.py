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
            query = 'SELECT date, time, subject, room, lecturer FROM training_schedule WHERE date >= date(\'now\')'
            self.cursor.execute(query)
            return self.cursor.fetchall()


    def get_subjects(self):
        """ Тащим из ДБ список предметов с фамилиями лекторов """
        with self.connection:
            self.cursor.execute('SELECT DISTINCT subject, materials, lecturer FROM training_schedule')
        return self.cursor.fetchall()


    def get_schedule_on_day(self, date):
        """ Принимаем на вход дату, тащим из ДБ расписание на эту дату """
        with self.connection:
            query = "SELECT time, subject, materials, room, lecturer FROM training_schedule WHERE date = date('{}') ".format(date)
            self.cursor.execute(query)
            return self.cursor.fetchall()


    def get_dates(self):
        """ Тащим из ДБ все имеющиеся даты без совпадений """
        with self.connection:
            self.cursor.execute('SELECT DISTINCT date FROM training_schedule WHERE date >= date(\'now\') ORDER BY date ')
        return self.cursor.fetchall()


    def close(self):
        """ Закрываем соединение с БД """
        self.connection.close()
