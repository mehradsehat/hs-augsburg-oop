from task_04_share import Share
import os


class Portfolio:
    def __init__(self, name, base_path):

        if not os.path.isdir(base_path):
            raise NotADirectoryError

        self.name = name
        self.base_path = base_path
        self.capital = 0.0
        self.shares = {}

    def change_available_capital(self, changed_capital):

        if self.capital + changed_capital >= 0:
            self.capital = self.capital + changed_capital
            return True
        else:
            return False

    def load_all_shares(self):

        files = os.listdir(self.base_path)

        for file_name in files:

            if file_name.endswith(".csv"):

                full_path = os.path.join(self.base_path, file_name)

                share = Share(full_path)

                share.load_data()

                self.shares[share.symbol] = share

    def purchase_sell_of(self, symbol, volume, date):

        if symbol not in self.shares:
            return False

        share = self.shares[symbol]

        try:
            share.set_current_price(date)
        except:
            return False

        trade_value = share.estimate_price(volume)

        # BUY
        if volume > 0:
            if self.capital >= trade_value:
                if share.purchase_sell(volume):
                    self.capital = self.capital - trade_value
                    return True
                else:
                    return False
            else:
                return False

        # SELL
        elif volume < 0:
            if abs(volume) <= share.purchased_volume:
                if share.purchase_sell(volume):
                    self.capital = self.capital + trade_value
                    return True
                else:
                    return False
            else:
                return False

        else:
            return False
