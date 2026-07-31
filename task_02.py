# Globale Variablen
name = ""
symbol = ""
datum = ""
purchase_price = 0.0
purchased_volume = 0
capital = 0.0
history = []  # [datum, current_stock_price, volume]


# Speichert den Namen und das Symbol einer Aktie
def set_stock(stock_name, stock_symbol):
    global name
    global symbol

    # Prüfen, ob beide Parameter Strings sind
    if isinstance(stock_name, str) and isinstance(stock_symbol, str):
        # Name und Symbol speichern
        name = stock_name
        symbol = stock_symbol

        return True
    else:
        return False


# Verändert das verfügbare Kapital
def change_available_capital(capital_change):
    global capital

    # Kapital erhöhen
    if capital_change > 0:
        capital = capital + capital_change
        return True

    # Keine Änderung
    elif capital_change == 0:
        return True

    # Kapital verringern
    else:
        # Prüfen, ob genügend Kapital vorhanden ist
        if abs(capital_change) > capital:
            return False
        else:
            capital = capital + capital_change
            return True


# Berechnet den Gewinn oder Verlust
def profit_or_loss(current_stock_price):
    global history

    result = 0.0
    for purchase in history:
        result += (current_stock_price - purchase[1]) * purchase[2]
    # (Aktueller Preis - Kaufpreis) × Anzahl der Aktien
    return result


# Berechnet das gesamte Kapital
def total_capital(current_stock_price):
    global capital
    global history

    # Gesamtvolumen aus der Historie berechnen
    purchased_volume = 0

    for purchase in history:
        purchased_volume += purchase[2]

    # Verfügbares Kapital + aktueller Wert der Aktien
    return purchased_volume * current_stock_price + capital


# Kauft oder verkauft Aktien
def purchase_sell(datum, current_stock_price, volume):
    global purchase_price
    global purchased_volume
    global capital
    global symbol
    global history

    datum = check_timestamp(datum)

    if datum == "":
        return False

    # Prüfen, ob das Symbol nur alphanumerische Zeichen enthält
    if not symbol.isalnum():
        return False

    # ---------------- Kaufen ----------------
    if volume > 0:

        # Kaufkosten berechnen
        purchase_cost = current_stock_price * volume

        # Prüfen, ob genügend Kapital vorhanden ist
        if purchase_cost > capital:
            return False

        # Kapital reduzieren
        capital = capital - purchase_cost

        # Aktienbestand erhöhen
        purchased_volume = purchased_volume + volume

        # Kaufpreis speichern
        purchase_price = current_stock_price
        # Kaufpreis und Volumen in der Historie speichern
        history.append([datum, current_stock_price, volume])

        return True

    # ---------------- Verkaufen ----------------
    elif volume < 0:

        # Prüfen, ob genügend Aktien vorhanden sind
        if abs(volume) > purchased_volume:
            return False

        # Verkaufserlös berechnen
        sale_income = current_stock_price * abs(volume)

        # Kapital erhöhen
        capital = capital + sale_income

        # Zu verkaufendes Volumen
        volume_to_sell = abs(volume)

        # Volumen aus der Historie reduzieren
        while volume_to_sell > 0:
            stored_volume = history[0][2]

            if volume_to_sell >= stored_volume:
                volume_to_sell = volume_to_sell - stored_volume
                history.pop(0)
            else:
                history[0][2] = stored_volume - volume_to_sell
                volume_to_sell = 0

        # Aktienbestand verringern
        purchased_volume = purchased_volume + volume

        # Historie löschen, wenn keine Aktien mehr vorhanden sind
        if purchased_volume == 0:
            history.clear()

        return True

    # Kein Kauf und kein Verkauf
    else:
        return False


def pretty_str(current_stock_price):
    global symbol
    global purchased_volume
    global capital

    # Prüfen, ob das Symbol gültig ist
    if not (isinstance(symbol, str) and symbol.isalnum()):
        return ""

    return (
        f"Aktiensymbol: {symbol}\n"
        f"Gekauftes Volumen: {purchased_volume}\n"
        f"Gewinn/Verlust: {profit_or_loss(current_stock_price):.2f} €\n"
        f"Gebundenes Kapital: {purchased_volume * current_stock_price:.2f} €\n"
        f"Verfügbares Kapital: {capital:.2f} €\n"
        f"Gesamtkapital: {total_capital(current_stock_price):.2f} €"
    )


def check_timestamp(timestamp: str) -> str:
    if not isinstance(timestamp, str):
        return ""

    # Tag.Monat.Jahr
    if "." in timestamp:
        if timestamp.count(".") != 2:
            return ""

        timestamp = timestamp.replace(".", "")

        if not timestamp.isdigit():  # ob Alle Zahlen sind oder nicht
            return ""

        if len(timestamp) == 6:
            day = timestamp[0:2]
            month = timestamp[2:4]
            year = int(timestamp[4:6])

            if year <= 49:
                year += 2000
            else:
                year += 1900

        elif len(timestamp) == 8:
            day = timestamp[0:2]
            month = timestamp[2:4]
            year = int(timestamp[4:8])

        else:
            return ""

    # Jahr-Monat-Tag
    elif "-" in timestamp:
        if timestamp.count("-") != 2:
            return ""

        timestamp = timestamp.replace("-", "")

        if not timestamp.isdigit():
            return ""

        if len(timestamp) == 8:
            year = int(timestamp[0:4])
            month = timestamp[4:6]
            day = timestamp[6:8]

        elif len(timestamp) == 6:
            year = int(timestamp[0:2])
            month = timestamp[2:4]
            day = timestamp[4:6]

            if year <= 49:
                year += 2000
            else:
                year += 1900

        else:
            return ""

    # JahrMonatTag
    else:
        if not timestamp.isdigit():
            return ""

        if len(timestamp) == 8:
            year = int(timestamp[0:4])
            month = timestamp[4:6]
            day = timestamp[6:8]

        elif len(timestamp) == 6:
            year = int(timestamp[0:2])
            month = timestamp[2:4]
            day = timestamp[4:6]

            if year <= 49:
                year += 2000
            else:
                year += 1900

        else:
            return ""

    # Erst jetzt können Monat und Tag geprüft werden
    month = int(month)
    day = int(day)

    if month < 1 or month > 12:
        return ""

    if day < 1 or day > 31:
        return ""

    return f"{year:04d}-{month:02d}-{day:02d}"  # Führende Nullen hinzufügen


def total_volume():
    global history

    volume = 0

    # Alle gekauften Aktien aufsummieren
    for purchase in history:
        volume += purchase[2]  # Index 2 : Volume

    return volume
