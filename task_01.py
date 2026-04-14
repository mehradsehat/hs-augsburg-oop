name = ""
symbol = ""
purchase_price = 0.0
purchased_volume = 0
capital = 0.0


def set_stock(stock_name, stock_symbol):
    global name, symbol
    if isinstance(stock_name, str) and isinstance(stock_symbol, str):
        name = stock_name
        symbol = stock_symbol
        return True
    else:
        return False


def change_available_capital(amount):
    global capital
    if not isinstance(amount, float):
        return False
    if amount + capital < 0:
        return False
    capital = capital + amount
    return True


def profit_or_loss(current_price):
    global purchase_price, purchased_volume
    if not isinstance(current_price, float):
        return 0.0
    profit = (current_price - purchase_price) * purchased_volume
    return profit


def total_capital(current_price):
    global capital, purchased_volume
    if not isinstance(current_price, float):
        return 0.0
    invested = current_price * purchase_price
    total = capital + invested
    return total


def purchase_sell(current_price, volume):
    global symbol, purchase_price, purchased_volume, capital
    if not isinstance(current_price, float):
        return False
    if not isinstance(capital, int):
        return False
    if not isinstance(symbol, str) or not symbol.isalnum():
        return False
    if volume > 0:
        cost = current_price * volume
        if cost > capital:
            return False
        capital = capital - cost
        purchased_volume += volume
        purchase_price = current_price
        return True
    elif volume < 0:
        sell_volume = sell_volume - volume
        if sell_volume > purchased_volume:
            return False
        capital += current_price * sell_volume
        purchased_volume -= sell_volume
        return True
    else:
        return False


def pretty_str(current_price):
    global symbol, purchased_volume, capital
    if not isinstance(symbol, str) or not symbol.isalnum():
        return ""

    profit = (current_price - purchase_price) * purchased_volume

    total = capital + (current_price * purchased_volume)

    result = f"Symbol: {symbol}"
    result += f"Volumen: {purchased_volume}"
    result += f"Gewinn/Verlust: {profit}"
    result += f"Kapital gesamt: {total}"
    result += f"Kapital frei: {capital}"

    return result


# test Case

print(set_stock("Appl inc.", "AALP"))
print(name)
print(symbol)
print(set_stock(4, "AALP"))
print(name)
print(symbol)
