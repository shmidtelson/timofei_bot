import telegram
import datetime
import configparser
from random_gif import GenerateGif

class Running:
    bot_token = ''
    chat_id = ''
    current_hi =[]

    def __init__(self):
        self.readConfig()
        self.bot = telegram.Bot(token=self.bot_token)
        self.sendMessage('Стартовал!')
        self.main()

    def readConfig(self):
        config = configparser.ConfigParser()
        config.read_file(open('settings.ini'))
        self.bot_token = config.get('default', 'bot_token')
        self.chat_id = config.get('default', 'chat_id')


    def main(self):
        while True:
            self.now = datetime.datetime.now()
            self.now_ymd = f'{self.now.year}-{self.now.month}-{self.now.day}'
            self.weekday = self.now.weekday()

            hi = f'{self.now.hour}-{self.now.minute}'

            if(self.validator(hi)):
                self.current_hi.append(hi)
                self.current_hi = self.current_hi[-2:]
                self.sendMessage(self.hi_and_messages(hi))

    def sendMessage(self, message):
        if message is not None:
            self.bot.sendMessage(chat_id=self.chat_id, text=message)


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
        if hi in ['9-45','11-45','13-45','15-45']:
            return 'Проветривание через 15 минут'

        if hi in ['10-00','12-00','14-00','16-00']:
            self.bot.sendDocument(chat_id=self.chat_id, document=GenerateGif().main())
            return 'Проветривание! Всем покинуть помещение!'

    def datesHolidays(self):
        return [
            '2018-12-24',
            '2018-12-25',
            '2018-12-31',
            '2018-1-1',
            '2018-1-7',
            '2018-1-8']

    def datesWork(self):
        return [
           '2018-12-22',
           '2018-12-29']

run = Running()