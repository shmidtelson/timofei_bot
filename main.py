#!/usr/local/bin/python3.7
import telegram
import datetime
import configparser
import os
from random_gif import GenerateGif

class Running:
    bot_token = ''
    chat_id = ''
    current_hi =[]

    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.readConfig()
        self.bot = telegram.Bot(token=self.bot_token)
        self.sendMessage('Стартовал!', self.chat_id)
        self.main()

    def readConfig(self):
        config = configparser.ConfigParser()
        config.read_file(open(os.path.join(self.script_dir, 'settings.ini')))
        self.bot_token = config.get('default', 'bot_token')
        self.chat_id = config.get('default', 'chat_id')
        self.group_id = config.get('default', 'group_id')

    def main(self):
        while True:
            self.now = datetime.datetime.now()
            self.now_ymd = f'{self.now.year}-{self.twoDigits(self.now.month)}-{self.twoDigits(self.now.day)}'
            self.weekday = self.now.weekday()

            hi = f'{self.twoDigits(self.now.hour)}-{self.twoDigits(self.now.minute)}'
            if(self.validator(hi)):
                self.current_hi.append(hi)
                self.current_hi = self.current_hi[-2:]
                self.sendMessage(self.hi_and_messages(hi), self.group_id)

    def sendMessage(self, message, chat_id):
        if message is not None:
            self.bot.sendMessage(chat_id=chat_id, text=message)


    def validator(self, hi):
        if self.isWeekend():
            return False

        if hi not in self.current_hi:
            return True

        return False

    def isWeekend(self):
        if self.now_ymd in self.datesHolidays():
            return True

        if self.now_ymd in self.datesWork():
            return False

        return self.weekday >= 5

    def hi_and_messages(self, hi):
        if hi in ['09-45','11-45','13-45','15-45']:
            return 'Проветривание через 15 минут'

        if hi in ['10-00','12-00','14-00','16-00']:
            self.bot.sendDocument(chat_id=self.group_id, document=GenerateGif().main())
            return 'Проветривание! Всем покинуть помещение!'

    def datesHolidays(self):
        return [
            '2018-12-24',
            '2018-12-25',
            '2018-12-31',
            '2018-01-01',
            '2019-01-07',
            ]

    def datesWork(self):
        return [
           '2018-12-22',
           '2018-12-29']

    def twoDigits(self, integer):
        return '{:02d}'.format(integer)

run = Running()
