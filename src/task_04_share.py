import datetime
import os


class Share:

    def purchase_sell(self, volume):

        if self.current_price == -1.0:
            return False

        # BUY
        if volume > 0:
            self.purchased_volume = self.purchased_volume + volume
            self.bound_capital = self.current_price * self.purchased_volume

            self.history.append([self.current_date, self.current_price, volume])

            return True

        # SELL
        elif volume < 0:
            if abs(volume) <= self.purchased_volume:
                self.purchased_volume = self.purchased_volume + volume
                self.bound_capital = self.current_price * self.purchased_volume

                sell_volume = abs(volume)

                while sell_volume > 0 and len(self.history) > 0:
                    first_trade = self.history[0]
                    first_trade_volume = first_trade[2]

                    if first_trade_volume <= sell_volume:
                        sell_volume = sell_volume - first_trade_volume
                        self.history.pop(0)
                    else:
                        first_trade[2] = first_trade_volume - sell_volume
                        sell_volume = 0

                if self.purchased_volume == 0:
                    self.history = []

                return True
            else:
                return False

        else:
            return False

    def total_volume(self):
        total = 0

        for trade in self.history:
            trade_volume = trade[2]
            total = total + trade_volume

        return total

    def __init__(self, path_to_csv_file, name=""):

        if not isinstance(path_to_csv_file, str):
            raise ValueError

        file_name = os.path.basename(path_to_csv_file)

        if "." not in file_name:
            raise ValueError

        self.symbol = file_name.rsplit(".", 1)[0]

        if self.symbol == "":
            raise ValueError

        self.path_to_csv_file = path_to_csv_file
        self.name = name

        self.current_price = -1.0
        self.current_date = datetime.date.today()
        self.profit_loss = 0.0
        self.bound_capital = 0.0
        self.purchased_volume = 0
        self.history = []
        self.stock_data = {}

    def set_current_price(self, date=""):

        try:
            self.current_date = check_timestamp(date)

            search_date = self.current_date
            found_price = None

            for i in range(6):
                date_key = str(search_date)

                if date_key in self.stock_data:
                    found_price = self.stock_data[date_key]
                    self.current_date = search_date
                    break

                search_date = search_date - datetime.timedelta(days=1)

            if found_price is None:
                raise LookupError

            self.current_price = found_price

            self.bound_capital = self.current_price * self.purchased_volume

            remaining_volume = self.purchased_volume
            total_purchase = 0.0

            for trade in reversed(self.history):
                trade_price = trade[1]
                trade_volume = trade[2]

                if trade_volume > 0:
                    if remaining_volume >= trade_volume:
                        total_purchase = total_purchase + trade_price * trade_volume
                        remaining_volume = remaining_volume - trade_volume
                    else:
                        total_purchase = total_purchase + trade_price * remaining_volume
                        remaining_volume = 0

                if remaining_volume == 0:
                    break

            current_value = self.current_price * self.purchased_volume
            self.profit_loss = current_value - total_purchase

        except:
            self.current_price = -1.0
            self.profit_loss = 0.0
            self.bound_capital = 0.0
            raise

    def load_data(self):

        if not os.path.exists(self.path_to_csv_file):
            return False

        try:
            with open(self.path_to_csv_file, "r") as file:
                lines = file.readlines()

                for line in lines[1:]:

                    try:
                        parts = line.strip().split(",")

                        date = parts[0]
                        close_price = float(parts[4])

                        self.stock_data[date] = close_price

                    except:
                        continue

            return True

        except:
            return False

    def estimate_price(self, volume):

        if self.current_price == -1.0:
            return 0.0

        estimate = self.current_price * abs(volume)

        return estimate

    def __str__(self):

        if self.symbol == "":
            return ""

        if self.current_price == -1.0:
            return ""

        output = (
            f"Symbol: {self.symbol}\n"
            f"Purchased Volume: {self.purchased_volume}\n"
            f"Profit/Loss: {self.profit_loss:.2f}\n"
            f"Bound Capital: {self.bound_capital:.2f}"
        )

        return output


def check_timestamp(timestamp):

    if not isinstance(timestamp, str):
        return datetime.date.today()

    if timestamp.isdigit():
        if len(timestamp) == 8:
            year = timestamp[0:4]
            month = timestamp[4:6]
            day = timestamp[6:8]

        elif len(timestamp) == 6:
            year = "20" + timestamp[0:2]
            month = timestamp[2:4]
            day = timestamp[4:6]

        else:
            return datetime.date.today()

    elif "." in timestamp:
        parts = timestamp.split(".")

        if len(parts) != 3:
            return datetime.date.today()

        day = parts[0]
        month = parts[1]
        year = parts[2]

        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            return datetime.date.today()

        if len(year) == 2:
            year = "20" + year

        elif len(year) != 4:
            return datetime.date.today()

    elif "-" in timestamp:
        parts = timestamp.split("-")

        if len(parts) != 3:
            return datetime.date.today()

        year = parts[0]
        month = parts[1]
        day = parts[2]

        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return datetime.date.today()

        if len(year) == 2:
            year = "20" + year

        elif len(year) != 4:
            return datetime.date.today()

    else:
        return datetime.date.today()

    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        return datetime.date.today()

    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return datetime.date.today()

    month_number = int(month)
    day_number = int(day)

    if month_number < 1 or month_number > 12:
        return datetime.date.today()

    if day_number < 1 or day_number > 31:
        return datetime.date.today()

    year = int(year)
    month = int(month)
    day = int(day)

    return datetime.date(year, month, day)
