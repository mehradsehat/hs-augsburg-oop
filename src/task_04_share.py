import datetime
import os


class Share:
    def __init__(self, path_to_csv_file, name=""):
        self.path_to_csv_file = path_to_csv_file
        self.name = name

        filename = os.path.basename(path_to_csv_file)
        symbol, extension = os.path.splitext(filename)

        if extension.lower() != ".csv":
            raise ValueError("Invalid CSV file.")

        self.symbol = symbol
        self.current_price = -1.0
        self.purchase_price = 0.0
        self.purchased_volume = 0
        self.current_date = datetime.date.today()
        self.profit_loss = 0.0
        self.bound_capital = 0.0
        self.history = []
        self.csv_data = []

    def estimate_price(self, volume):
        if self.current_price == -1.0:
            return 0.0

        return self.current_price * volume

    def set_current_price(self, date_str=""):
        try:
            self.current_date = check_timestamp(date_str)

            search_date = self.current_date
            found_price = None

            for day_back in range(0, 6):
                for item in self.csv_data:
                    if item[0] == search_date:
                        found_price = item[1]
                        break

                if found_price is not None:
                    break

                search_date = search_date - datetime.timedelta(days=1)

            if found_price is None:
                self.current_price = -1.0
                self.profit_loss = 0.0
                self.bound_capital = 0.0
                raise LookupError("No Close Price Found For This Date")

            self.current_date = search_date
            self.current_price = found_price

            self.profit_loss = self.current_price * self.purchased_volume

            for item in self.history:
                self.profit_loss = self.profit_loss - (item[1] * item[2])

            self.bound_capital = self.current_price * self.purchased_volume

        except:
            self.current_price = -1.0
            self.profit_loss = 0.0
            self.bound_capital = 0.0
            raise

    def load_data(self):
        if not os.path.exists(self.path_to_csv_file):
            return False

        try:
            file = open(self.path_to_csv_file, "r")
            lines = file.readlines()
            file.close()

            self.csv_data.clear()

            for i in range(1, len(lines)):
                try:
                    values = lines[i].split(",")
                    date_obj = check_timestamp(values[0])
                    close_price = float(values[4])
                    self.csv_data.append([date_obj, close_price])

                except:
                    continue

            return True

        except:
            return False

    def total_volume(self):
        volume = 0

        for item in self.history:
            volume += item[2]

        return volume

    def purchase_sell(self, volume):
        if self.current_price == -1.0:
            return False

        if volume > 0:
            self.purchased_volume += volume
            self.purchase_price = self.current_price
            self.history.append([self.current_date, self.current_price, volume])
            return True

        elif volume < 0:
            if self.purchased_volume >= abs(volume):
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
