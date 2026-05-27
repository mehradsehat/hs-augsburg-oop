name = ""
symbol = ""
purchase_price = 0.0
purchased_volume = 0
capital = 0.0
history = []


def set_stock(stock_name, stock_symbol):

    global name
    global symbol

    if isinstance(stock_name, str) and isinstance(stock_symbol, str):
        name = stock_name
        symbol = stock_symbol
        return True
    else:
        return False


def change_available_capital(amount):

    global capital

    if capital + amount >= 0:
        capital += amount
        return True
    else:
        return False


def profit_or_loss(current_price):

    global history
    global purchased_volume

    profit = current_price * purchased_volume

    for item in history:
        profit = profit - (item[1] * item[2])

    return profit


def total_volume():

    volume = 0

    for item in history:
        volume = volume + item[2]

    return volume


def total_capital(current_price):

    global capital
    global purchase_price
    global purchased_volume

    volume = 0

    for item in history:
        volume = volume + item[2]

    return capital + (current_price * volume)


def purchase_sell(date_str, current_price, volume):

    global capital
    global purchase_price
    global purchased_volume
    global symbol
    global history

    if not symbol.isalnum():
        return False

    if check_timestamp(date_str) == "":
        return False

    if volume > 0:
        if capital >= current_price * volume:
            capital = capital - (current_price * volume)
            purchased_volume += volume
            purchase_price = current_price
            history.append([date_str, current_price, volume])
            return True
        else:
            return False

    elif volume < 0:
        if purchased_volume >= abs(volume):
            capital = capital + (current_price * abs(volume))
            purchased_volume -= abs(volume)
            if purchased_volume == 0:
                history.clear()
            return True
        else:
            return False

    else:
        return False


def pretty_str(date_str, current_price):

    global symbol
    global capital
    global purchased_volume
    global purchase_price

    if not symbol.isalnum():
        return ""

    profit_loss = (current_price - purchase_price) * purchased_volume
    total = capital + (current_price * purchased_volume)

    return (
        f"Symbol: {symbol}\n"
        f"Date: {check_timestamp(date_str)}"
        f"Purchased Volume: {purchased_volume}\n"
        f"Profit/Loss: {profit_loss}\n"
        f"Total Capital: {total}\n"
        f"Total Volume: {total_volume()}"
    )


def check_timestamp(date_str):

    if len(date_str) == 0 or not isinstance(date_str, str):
        return ""

    # JahrMonatTag
    if len(date_str) == 8 and "." not in date_str and "-" not in date_str:
        year = date_str[0:4]
        month = date_str[4:6]
        day = date_str[6:8]

        return year + "-" + month + "-" + day

    if len(date_str) == 6 and "." not in date_str and "-" not in date_str:
        year = date_str[0:2]
        month = date_str[2:4]
        day = date_str[4:6]

        return "20" + year + "-" + month + "-" + day

    # Tag.Monat.Jahr
    if "." in date_str:
        if len(date_str) == 10:
            day = date_str[0:2]
            month = date_str[3:5]
            year = date_str[6:10]

            return year + "-" + month + "-" + day

        if len(date_str) == 8:
            day = date_str[0:2]
            month = date_str[3:5]
            year = date_str[6:8]

            return "20" + year + "-" + month + "-" + day

    # Jahr-Monat-Tag
    if "-" in date_str:
        if len(date_str) == 10:
            year = date_str[0:4]
            month = date_str[5:7]
            day = date_str[8:10]

            return year + "-" + month + "-" + day

        if len(date_str) == 8:
            year = date_str[0:2]
            month = date_str[3:5]
            day = date_str[6:8]

            return "20" + year + "-" + month + "-" + day

    return ""
