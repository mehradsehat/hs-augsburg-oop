import argparse
import logging
import sys

from task_06_portfolio import Portfolio

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
log.addHandler(handler)


class PortfolioCMD:

    def __init__(self):

        log.info("PortfolioCMD started")

        if len(sys.argv) != 3:
            log.error("Wrong amount of start arguments")
            raise SystemError

        parser = argparse.ArgumentParser()

        parser.add_argument("name")
        parser.add_argument("path")

        args = parser.parse_args()

        self.portfolio = Portfolio(args.name, args.path)
        self.portfolio.load_all_shares()
        self.api_key = "demo"

    def evaluate_user_input(self, cmd_input=""):

        log.info(f"User Input: {cmd_input}")

        if cmd_input == "":
            return True

        sys.argv = [__file__] + cmd_input.split()

        parser = argparse.ArgumentParser()

        parser.add_argument("-q", "--quit", action="store_true")
        parser.add_argument("-s", "--set_capital", type=float)
        parser.add_argument("-c", "--capital", action="store_true")
        parser.add_argument("-o", "--order", nargs=3)
        parser.add_argument("-d", "--date")
        parser.add_argument("-l", "--list_symbols", action="store_true")
        parser.add_argument("-lp", "--list_profit", action="store_true")
        parser.add_argument("-ll", "--list_loss", action="store_true")
        parser.add_argument("-f", "--filter")
        parser.add_argument("-a", "--add", nargs="+")
        parser.add_argument("-u", "--update", action="store_true")
        parser.add_argument("-k", "--apikey")

        try:
            args = parser.parse_args()

        except SystemExit:
            log.error("Invalid command entered")
            return True

        if args.quit:
            self.portfolio.shutdown()
            return False

        if args.set_capital is not None:
            self.portfolio.change_available_capital(args.set_capital)
            return True

        if args.capital:
            print(f"---- Aktuelles Kapital: {self.portfolio.capital}")
            return True

        if args.apikey is not None:
            self.api_key = args.apikey
            return True

        if args.add is not None:
            for symbol in args.add:
                self.portfolio.add_share(symbol)

            return True

        if args.update:
            failed_symbols = self.portfolio.update_all(self.api_key)

            if len(failed_symbols) > 0:
                print(
                    f"Daten der Aktien {failed_symbols} "
                    f"konnten nicht gefunden werden"
                )

            return True

        if args.order is not None:
            symbol = args.order[0]

            try:
                volume = int(args.order[1])
            except:
                return True

            date_str = args.order[2]

            self.portfolio.purchase_sell_of(symbol, volume, date_str)

            return True

        if args.date is not None:
            for share in self.portfolio:
                try:
                    share.set_current_price(args.date)
                except:
                    pass

            return True

        shares = list(self.portfolio)

        if args.filter is not None:
            shares = [share for share in shares if args.filter in share.symbol]

        if args.list_symbols:
            shares.sort(key=lambda share: share.symbol)

            for share in shares:
                print(share)

            return True

        if args.list_profit:
            shares.sort(reverse=True)

            for share in shares:
                print(share)

            return True

        if args.list_loss:
            shares.sort()

            for share in shares:
                print(share)

            return True

        return True


if __name__ == "__main__":
    p = PortfolioCMD()
    interaction_loop = True
    while interaction_loop:
        cmd = input("--> Ihre Eingabe (-q Ende): ")
        interaction_loop = p.evaluate_user_input(cmd)


# ---------------- TEST COMMANDS ----------------
# Terminal:
# cd /Users/mehrad/hs-augsburg-oop/src
#
# Start program:
# python3 task_07_cmd.py MyPortfolio ../stock_data
#
# Set API key:
# -k YONCZ9QIY7CJVITA
#
# Add shares:
# -a IBM
#
# Update data:
# -u
#
# Set date:
# -d 20.04.2020
#
# List by symbol:
# -l
#
# List by profit:
# -lp
#
# List by loss:
# -ll
#
# Filter by symbol:
# -l -f A
#
# Same filter, different order:
# -f A -ll
#
# Quit and save:
# -q
# -----------------------------------------------
