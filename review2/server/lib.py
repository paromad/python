import json
import random

start_capital = 10000


class User:
    def __init__(self):
        self.money = start_capital
        self.stocks = {}
        self.putting_money = 0

    def get_profit(self):
        return self.money - self.putting_money - start_capital

    def put_money(self, amount):
        self.money += amount
        self.putting_money += amount

    def subtract_money(self, amount):
        self.money -= amount

    def quantity_of_money(self):
        return self.money

    def get_users_stocks(self):
        return self.stocks

    def buy_stocks(self, burse, stock, amount):
        value = burse.get_value(stock) * amount
        if value <= self.money:
            self.subtract_money(value)
            self.stocks.setdefault(stock, 0)
            self.stocks[stock] += amount
            burse.update()
            return "Success"
        return "Failed"

    def sell_stocks(self, burse, stock, amount):
        if stock in self.stocks:
            if self.stocks[stock] >= amount:
                self.stocks[stock] -= amount
                if self.stocks[stock] == 0:
                    self.stocks.pop(stock)
                self.money += burse.get_value(stock) * amount
                burse.update()
                return "Success"
        return "Failed"


class Burse:
    def __init__(self):
        with open("burse.txt", "r") as f:
            self.stocks = json.load(f)
        with open("limits.txt", "r") as f:
            self.limits = json.load(f)

    def update(self):
        for stock in self.stocks:
            self.stocks[stock] = random.randint(self.limits["min"],
                                                self.limits["max"])
            json.dump(self.stocks, open("burse.txt", "w"))

    def get_prices(self):
        return self.stocks

    def get_value(self, stock):
        return self.stocks[stock]
