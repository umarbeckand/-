import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        if date:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
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
        return sum(r.amount for r in self.records if r.date == today)

    def get_week_stats(self):
        today = dt.datetime.now().date()
        week_ago = today - dt.timedelta(days=7)
        return sum(r.amount for r in self.records if week_ago < r.date <= today)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remained = self.limit - self.get_today_stats()
        if remained > 0:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained} кКал"
        return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE = 91.0
    EURO_RATE = 98.0

    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
        }

        rate, currency_name = currencies.get(currency, (None, None))
        if rate is None:
            return "Неверная валюта"

        cash_remained = self.limit - self.get_today_stats()
        cash_converted = round(cash_remained / rate, 2)

        if cash_remained > 0:
            return f"На сегодня осталось {cash_converted} {currency_name}"
        elif cash_remained == 0:
            return "Денег нет, держись"
        return f"Денег нет, держись: твой долг - {abs(cash_converted)} {currency_name}"
r1 = Record(amount=100, comment="Шаурма")
cash_calc = CashCalculator(1000)

cash_calc.add_record(r1)

print(cash_calc.get_today_cash_remained("rub"))
