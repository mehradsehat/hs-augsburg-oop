import datetime
import os
import urllib.request
import urllib.parse
import ssl


class Share:

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

    def update(self, api_key="demo"):

        try:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": self.symbol,
                "apikey": api_key,
                "datatype": "csv",
            }

            url = "https://www.alphavantage.co/query?" + urllib.parse.urlencode(params)
            context = ssl._create_unverified_context()

            with urllib.request.urlopen(url, context=context) as response:
                data = response.read().decode("utf-8")

            lines = data.splitlines()

            if len(lines) <= 1:
                return False

            if not lines[0].startswith("timestamp"):
                return False

            for line in lines[1:]:

                parts = line.split(",")

                if len(parts) < 6:
                    continue

                date = parts[0]

                self.stock_data[date] = {
                    "open": float(parts[1]),
                    "high": float(parts[2]),
                    "low": float(parts[3]),
                    "close": float(parts[4]),
                    "adj_close": 0.0,
                    "volume": int(parts[5]),
                }

            return True

        except:
            return False

    def save_data(self):

        if len(self.stock_data) == 0:
            return False

        try:
            file = open(self.path_to_csv_file, "w")

            file.write("Date,Open,High,Low,Close,Adj Close,Volume\n")

            for date in sorted(self.stock_data.keys(), reverse=True):
                data = self.stock_data[date]

                file.write(
                    f"{date},"
                    f"{data['open']},"
                    f"{data['high']},"
                    f"{data['low']},"
                    f"{data['close']},"
                    f"{data['adj_close']},"
                    f"{data['volume']}\n"
                )

            file.close()

            return True

        except:
            return False

    def load_data(self):

        if not os.path.exists(self.path_to_csv_file):
            return False

        try:
            with open(self.path_to_csv_file, "r") as file:
                lines = file.readlines()

                for line in lines[1:]:

                    try:
                        parts = line.strip().split(",")

                        if len(parts) < 7:
                            continue

                        date = parts[0]

                        self.stock_data[date] = {
                            "open": float(parts[1]),
                            "high": float(parts[2]),
                            "low": float(parts[3]),
                            "close": float(parts[4]),
                            "adj_close": float(parts[5]),
                            "volume": int(float(parts[6])),
                        }

                    except:
                        continue

            return True

        except:
            return False

    def set_current_price(self, date=""):

        try:
            self.current_date = check_timestamp(date)

            search_date = self.current_date
            found_price = None

            for i in range(6):
                date_key = str(search_date)

                if date_key in self.stock_data:
                    found_price = self.stock_data[date_key]["close"]
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

    def purchase_sell(self, volume):

        if self.current_price == -1.0:
            return False

        if volume > 0:
            self.purchased_volume = self.purchased_volume + volume
            self.bound_capital = self.current_price * self.purchased_volume
            self.history.append([self.current_date, self.current_price, volume])
            return True

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

            return False

        return False

    def total_volume(self):
        total = 0

        for trade in self.history:
            total = total + trade[2]

        return total

    def estimate_price(self, volume):

        if self.current_price == -1.0:
            return 0.0

        return self.current_price * abs(volume)

    def __str__(self):

        if self.symbol == "":
            return ""

        if self.current_price == -1.0:
            return ""

        return (
            f"Symbol: {self.symbol}\n"
            f"Purchased Volume: {self.purchased_volume}\n"
            f"Profit/Loss: {self.profit_loss:.2f}\n"
            f"Bound Capital: {self.bound_capital:.2f}"
        )

    def __lt__(self, other):
        return self.profit_loss < other.profit_loss

    def __le__(self, other):
        return self.profit_loss <= other.profit_loss

    def __eq__(self, other):
        return self.profit_loss == other.profit_loss

    def __ne__(self, other):
        return self.profit_loss != other.profit_loss

    def __gt__(self, other):
        return self.profit_loss > other.profit_loss

    def __ge__(self, other):
        return self.profit_loss >= other.profit_loss


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
