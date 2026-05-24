name = ""
symbol = ""
purchase_price = 0.0
purchased_volume = 0
capital = 0.0
history = []


def set_stock(new_name, new_symbol):
    global name
    global symbol

    if isinstance(new_name, str) and isinstance(new_symbol, str):
        name = new_name
        symbol = new_symbol
        return True
    else:
        return False


def change_available_capital(changed_capital):
    global capital

    if capital + changed_capital >= 0:
        capital = capital + changed_capital
        return True
    else:
        return False


def profit_or_loss(current_price):
    global history
    global purchased_volume

    remaining_volume = purchased_volume
    total_purchase = 0.0

    for trade in reversed(history):
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

    current_value = current_price * purchased_volume

    return current_value - total_purchase


def total_capital(current_stock_value):
    global capital
    global purchased_volume

    invested_money = current_stock_value * purchased_volume

    return capital + invested_money


def purchase_sell(timestamp, current_price, volume):
    global symbol
    global purchase_price
    global purchased_volume
    global capital
    global history

    checked_timestamp = check_timestamp(timestamp)
    if checked_timestamp == "":
        return False

    if not symbol.isalnum():
        return False

    trade_value = current_price * abs(volume)

    # BUY
    if volume > 0:
        if capital >= trade_value:
            capital = capital - trade_value
            purchased_volume = purchased_volume + volume
            purchase_price = current_price

            history.append([checked_timestamp, current_price, volume])

            return True
        else:
            return False

    # SELL
    elif volume < 0:
        if abs(volume) <= purchased_volume:
            capital = capital + trade_value
            purchased_volume = purchased_volume + volume

            sell_volume = abs(volume)

            while sell_volume > 0 and len(history) > 0:
                first_trade = history[0]
                first_trade_volume = first_trade[2]

                if first_trade_volume <= sell_volume:
                    sell_volume = sell_volume - first_trade_volume
                    history.pop(0)
                else:
                    first_trade[2] = first_trade_volume - sell_volume
                    sell_volume = 0

            if purchased_volume == 0:
                history = []

            return True
        else:
            return False

    else:
        return False


def pretty_str(current_stock_value):
    global symbol
    global purchased_volume
    global capital

    if not symbol.isalnum():
        return ""

    profit = profit_or_loss(current_stock_value)
    total = total_capital(current_stock_value)

    output = (
        f"Symbol: {symbol}\n"
        f"Purchased Volume: {purchased_volume}\n"
        f"Profit/Loss: {profit}\n"
        f"Available Capital: {capital}\n"
        f"Total Capital: {total}"
    )

    return output


def check_timestamp(timestamp):
    if not isinstance(timestamp, str):
        return ""

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
            return ""

    elif "." in timestamp:
        parts = timestamp.split(".")

        if len(parts) != 3:
            return ""

        day = parts[0]
        month = parts[1]
        year = parts[2]

        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            return ""

        if len(year) == 2:
            year = "20" + year
        elif len(year) != 4:
            return ""

    elif "-" in timestamp:
        parts = timestamp.split("-")

        if len(parts) != 3:
            return ""

        year = parts[0]
        month = parts[1]
        day = parts[2]

        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return ""

        if len(year) == 2:
            year = "20" + year
        elif len(year) != 4:
            return ""

    else:
        return ""

    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        return ""

    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return ""

    month_number = int(month)
    day_number = int(day)

    if month_number < 1 or month_number > 12:
        return ""

    if day_number < 1 or day_number > 31:
        return ""

    return year + "-" + month + "-" + day


def total_volume():
    global history

    total = 0

    for trade in history:
        trade_volume = trade[2]
        total = total + trade_volume

    return total
