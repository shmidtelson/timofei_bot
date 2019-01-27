import requests

# Dates documentation is here https://isdayoff.ru/desc/

class ParseHoliday:
    country = 'by'
    url = f'https://isdayoff.ru/%s?cc={country}'
    date = ''

    def __init__(self, date):
        self.date = date
        self.result = self.getData()

    def getData(self): # YYYYMMDD
        try:
            print(self.url)
            r = requests.get(self.url % self.date)
            return r.text
        except Exception as e:
            print(e)