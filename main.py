#!/usr/local/bin/python3.7
import telegram
import datetime
import configparser
import os
from random_gif import GenerateGif
from holiday_checker_api import ParseHoliday

class Running:
    bot_token = ''
    chat_id = ''
    current_hi =[] # latest 3 minutes
    current_parse_date = '' # YYYYMMDD
    current_status_day = '' # 1/0 Holiday or no

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

            month = self.twoDigits(self.now.month)
            day = self.twoDigits(self.now.day)

            self.currentDate(f'{self.now.year}{month}{day}')

            self.now_ymd = f'{self.now.year}-{month}-{day}'
            self.weekday = self.now.weekday()

            hi = f'{self.twoDigits(self.now.hour)}-{self.twoDigits(self.now.minute)}'

            if(self.current_status_day == '1'):
                continue

            if(hi in self.current_hi):
                continue

            self.current_hi.append(hi)
            self.current_hi = self.current_hi[-2:]
            self.sendMessage(self.hi_and_messages(hi), self.group_id)

    def sendMessage(self, message, chat_id):
        if message is not None:
            self.bot.sendMessage(chat_id=chat_id, text=message)

    def hi_and_messages(self, hi):
        if hi in ['09-45','11-45','13-45','15-45']:
            return 'Проветривание через 15 минут'

        if hi in ['10-00','12-00','14-00','16-00']:
            self.bot.sendDocument(chat_id=self.group_id, document=GenerateGif().main())
            return 'Проветривание! Всем покинуть помещение!'

    def currentDate(self, date):
        if(self.current_parse_date != date):
            self.current_parse_date = date
            c = ParseHoliday(self.current_parse_date)
            self.current_status_day = c.result

    def twoDigits(self, integer):
        return '{:02d}'.format(integer)

run = Running()
