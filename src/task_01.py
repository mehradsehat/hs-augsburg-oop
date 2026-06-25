name = ""
symbol = ""
purchase_price = 0.0
purchased_volume = 0
capital = 0.0


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

    global purchase_price
    global purchased_volume

    return (current_price - purchase_price) * purchased_volume


def total_capital(current_price):

    global capital
    global purchase_price
    global purchased_volume

    return capital + (current_price * purchased_volume)


def purchase_sell(current_price, volume):

    global capital
    global purchase_price
    global purchased_volume
    global symbol

    if not symbol.isalnum():
        return False

    if volume > 0:
        if capital >= current_price * volume:
            capital = capital - (current_price * volume)
            purchased_volume += volume
            purchase_price = current_price
            return True
        else:
            return False

    elif volume < 0:
        if purchased_volume >= abs(volume):
            capital = capital + (current_price * abs(volume))
            purchased_volume -= abs(volume)
            return True
        else:
            return False

    else:
        return False


def pretty_str(current_price):

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
        f"Purchased Volume: {purchased_volume}\n"
        f"Profit/Loss: {profit_loss}\n"
        f"Total Capital: {total}"
    )
