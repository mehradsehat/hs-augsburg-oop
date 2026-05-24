name = ""
symbol = ""
purchase_price = 0.0
purchased_volume = 0
capital = 0.0


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

    global purchase_price
    global purchased_volume

    total_purchase = purchase_price * purchased_volume

    current_value = current_price * purchased_volume

    return current_value - total_purchase


def total_capital(current_stock_value):

    global capital
    global purchased_volume

    invested_money = current_stock_value * purchased_volume

    return capital + invested_money


def purchase_sell(current_price, volume):

    global symbol
    global purchase_price
    global purchased_volume
    global capital

    if not symbol.isalnum():

        return False

    trade_volume = current_price * abs(volume)

    # BUY
    if volume > 0:

        if capital >= trade_volume:

            capital = capital - trade_volume

            purchased_volume = purchased_volume + volume

            purchase_price = current_price

            return True

        else:

            return False

    # SELL
    elif volume < 0:

        if abs(volume) <= purchased_volume:

            capital = capital + trade_volume

            purchased_volume = purchased_volume + volume

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


"""
# Correct test
print(set_stock("Apple", "AAPL"))
print(change_available_capital(1000.0))
print(purchase_sell(100.0, 3))
print(pretty_str(120.0))
"""

# Wrong test
print(purchase_sell(500.0, 10))
print(pretty_str(120.0))
