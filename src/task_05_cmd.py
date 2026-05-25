import argparse
import logging
import sys

from task_04_portfolio import Portfolio

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

        log.info(f"Portfolio Name: {args.name}")
        log.info(f"CSV Path: {args.path}")

        self.portfolio = Portfolio(args.name, args.path)

        log.info("Portfolio created successfully")

        self.portfolio.load_all_shares()

        log.info("All shares loaded")

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

        try:
            args = parser.parse_args()

        except SystemExit:
            log.error("Invalid command entered")
            return True

        if args.quit:
            log.info("Program terminated")
            return False

        if args.set_capital is not None:

            log.info(f"Capital changed by {args.set_capital}")

            self.portfolio.change_available_capital(args.set_capital)

            return True

        if args.capital:

            log.info(f"Current capital: {self.portfolio.capital}")

            print(f"---- Aktuelles Kapital: " f"{self.portfolio.capital}")

            return True

        if args.order is not None:

            symbol = args.order[0]

            volume = int(args.order[1])

            date_str = args.order[2]

            log.info(
                f"Order: " f"Symbol={symbol}, " f"Volume={volume}, " f"Date={date_str}"
            )

            self.portfolio.purchase_sell_of(symbol, volume, date_str)

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
# python3 task_05_cmd.py MyPortfolio ../stock_data
#
# Add capital:
# -s 25000
#
# Show capital:
# -c
#
# Buy 10 AAPL shares:
# -o AAPL 10 12.04.24
#
# Show capital again:
# -c
#
# Sell 5 AAPL shares:
# -o AAPL -5 24-04-22
#
# Quit program:
# -q
# -----------------------------------------------
