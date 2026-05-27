import datetime

capital = 0.0


class Share:
    def __init__(self, name, symbol):

        if isinstance(name, str) and isinstance(symbol, str):
            self.name = name
            self.symbol = symbol
        else:
            self.name = ""
            self.symbol = ""

        self.current_price = -1.0
        self.purchase_price = 0.0
        self.purchased_volume = 0
        self.current_date = datetime.date.today()
        self.profit_loss = 0.0
        self.bound_capital = 0.0
        self.history = []  # date_str, current_price, volume

    def set_current_price(self, current_price, date_str=""):
        if not isinstance(current_price, (int, float)):
            self.current_price = -1.0
            self.profit_loss = 0.0
            self.bound_capital = 0.0
            return False

        self.current_date = check_timestamp(date_str)
        self.current_price = float(current_price)

        self.profit_loss = self.current_price * self.purchased_volume

        for item in self.history:
            self.profit_loss = self.profit_loss - (item[1] * item[2])

        self.bound_capital = self.current_price * self.purchased_volume

        return True

    def total_volume(self):
        volume = 0

        for item in self.history:
            volume += item[2]

        return volume

    def purchase_sell(self, volume):
        global capital

        if self.current_price == -1.0:
            return False

        if volume > 0:

            if capital >= self.current_price * volume:

                capital -= self.current_price * volume

                self.purchased_volume += volume

                self.purchase_price = self.current_price

                self.history.append([self.current_date, self.current_price, volume])

                return True

            else:
                return False

        elif volume < 0:

            if self.purchased_volume >= abs(volume):

                capital += self.current_price * abs(volume)

                self.purchased_volume -= abs(volume)

                self.history.append([self.current_date, self.current_price, volume])

                if self.purchased_volume == 0:
                    self.history.clear()

                return True

            else:
                return False

        else:
            return False

    def __str__(self):

        if self.symbol == "" or self.current_price == -1.0:
            return ""

        return (
            f"Name: {self.name}\n"
            f"Symbol: {self.symbol}\n"
            f"Current Price: {self.current_price}\n"
            f"Current Date: {self.current_date}\n"
            f"Purchased Volume: {self.purchased_volume}\n"
            f"Profit/Loss: {self.profit_loss}\n"
            f"Bound Capital: {self.bound_capital}\n"
            f"Total Volume: {self.total_volume()}"
        )


def change_available_capital(amount):

    global capital

    if capital + amount >= 0:
        capital += amount
        return True
    else:
        return False


def check_timestamp(date_str):

    if not isinstance(date_str, str) or len(date_str) == 0:
        return datetime.date.today()

    if len(date_str) == 8 and "." not in date_str and "-" not in date_str:
        date_obj = datetime.datetime.strptime(date_str, "%Y%m%d")
        return date_obj.date()

    if len(date_str) == 6 and "." not in date_str and "-" not in date_str:
        date_obj = datetime.datetime.strptime(date_str, "%y%m%d")
        return date_obj.date()

    if "." in date_str:
        if len(date_str) == 10:
            date_obj = datetime.datetime.strptime(date_str, "%d.%m.%Y")
            return date_obj.date()

        if len(date_str) == 8:
            date_obj = datetime.datetime.strptime(date_str, "%d.%m.%y")
            return date_obj.date()

    if "-" in date_str:
        if len(date_str) == 10:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.date()

        if len(date_str) == 8:
            date_obj = datetime.datetime.strptime(date_str, "%y-%m-%d")
            return date_obj.date()

    return datetime.date.today()
