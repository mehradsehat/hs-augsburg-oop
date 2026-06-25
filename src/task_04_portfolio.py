import os
from task_04_share import Share


class Portfolio:

    def __init__(self, name, base_path):

        self.name = name

        if not os.path.isdir(base_path):
            raise NotADirectoryError("Directory not found.")

        self.base_path = base_path
        self.capital = 0.0
        self.shares = []

    def change_available_capital(self, amount):

        if self.capital + amount >= 0:
            self.capital += amount
            return True

        return False

    def purchase_sell_of(self, symbol, volume, date_str):

        for share in self.shares:

            if share.symbol == symbol:

                try:
                    share.set_current_price(date_str)

                    value = share.estimate_price(volume)

                    if volume > 0:

                        if self.capital < value:
                            return False

                        if share.purchase_sell(volume):
                            self.capital -= value
                            return True

                        return False

                    elif volume < 0:

                        if share.purchase_sell(volume):
                            self.capital -= value
                            return True

                        return False

                    return False

                except:
                    return False

        return False
