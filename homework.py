import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        self.date = date
        if self.date != '':
            date_format = '%d.%m.%Y'
            moment = dt.datetime.strptime(date, date_format)
            day = moment.date()
            self.date = day
        else:
            self.date = dt.datetime.now().date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.datetime.now().date()
        today_amount = 0
        for i in range(0, len(self.records)):
            rec = self.records[i]
            if rec.date == today:
                today_amount += rec.amount
        return today_amount

    def get_week_stats(self):
        today = dt.datetime.now().date()
        last_week_day = today - dt.timedelta(days=7)
        week_amount = 0
        for i in range(0, len(self.records)):
            rec = self.records[i]
            if last_week_day <= rec.date <= today:
                week_amount += rec.amount
        return week_amount


class CashCalculator(Calculator):
    USD_RATE = 72.81
    EURO_RATE = 89.11
    rates = {'usd': (USD_RATE, 'USD'),
             'eur': (EURO_RATE, 'Euro'),
             'rub': (1, 'руб')
             }

    def get_today_cash_remained(self, currency):
        today_cash_remained = self.limit - self.get_today_stats()
        for cur in self.rates:
            if currency == cur:
                rate = self.rates[cur][0]
                currency_name = self.rates[cur][1]
                if today_cash_remained > 0:
                    currency_convert = round(today_cash_remained / rate, 2)
                    return f'На сегодня осталось {currency_convert} {currency_name}'
                elif today_cash_remained < 0:
                    currency_convert = abs(round(today_cash_remained / rate, 2))
                    return f'Денег нет, держись: твой долг - {currency_convert} {currency_name}'
                else:
                    return f'Денег нет, держись'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_calories_balance = self.limit - self.get_today_stats()
        if today_calories_balance > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {today_calories_balance} кКал')
        else:
            return f'Хватит есть!'
