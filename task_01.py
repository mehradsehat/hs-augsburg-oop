# Globale Variablen
name = ""
symbol = ""
purchase_price = 0.0
purchased_volume = 0
capital = 0.0


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
    global purchase_price
    global purchased_volume

    # (Aktueller Preis - Kaufpreis) × Anzahl der Aktien
    return (current_stock_price - purchase_price) * purchased_volume


# Berechnet das gesamte Kapital
def total_capital(current_stock_price):
    global purchased_volume
    global capital

    # Verfügbares Kapital + aktueller Wert der Aktien
    return purchased_volume * current_stock_price + capital


# Kauft oder verkauft Aktien
def purchase_sell(current_stock_price, volume):
    global purchase_price
    global purchased_volume
    global capital
    global symbol

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

        # Aktienbestand verringern
        purchased_volume = purchased_volume + volume

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


"""
ÜBERSICHT DER GLOBALEN VARIABLEN
--------------------------------

name:
Name der Aktie.
Beispiel: "Apple"

symbol:
Kurzzeichen der Aktie.
Beispiel: "AAPL"

purchase_price:
Preis pro Aktie beim letzten Kauf.

purchased_volume:
Anzahl der aktuell vorhandenen Aktien.

capital:
Aktuell verfügbares Bargeld.


1. FUNKTION: set_stock(stock_name, stock_symbol)
------------------------------------------------

Aufgabe:
Speichert den Namen und das Symbol der Aktie.

Parameter:
stock_name:
Name der Aktie als String.

stock_symbol:
Symbol der Aktie als String.

Bedingung:
Beide Parameter müssen vom Typ str sein.

Prüfung:
isinstance(stock_name, str)
und
isinstance(stock_symbol, str)

Änderung:
name = stock_name
symbol = stock_symbol

Rückgabewert:
True:
Name und Symbol wurden erfolgreich gespeichert.

False:
Mindestens ein Parameter ist kein String.


2. FUNKTION: change_available_capital(capital_change)
------------------------------------------------------

Aufgabe:
Erhöht oder verringert das verfügbare Kapital.

Parameter:
capital_change:
Änderung des Kapitals.

capital_change > 0:
Kapital wird erhöht.

capital_change < 0:
Kapital wird verringert.

capital_change == 0:
Kapital bleibt unverändert.

Formel:
Neues Kapital = altes Kapital + Kapitaländerung

Python:
capital = capital + capital_change

Bedingung beim Verringern:
Das Kapital darf niemals negativ werden.

Prüfung:
abs(capital_change) <= capital

oder allgemein:
capital + capital_change >= 0

Rückgabewert:
True:
Die Änderung wurde durchgeführt.

False:
Die Änderung würde das Kapital negativ machen.


3. FUNKTION: profit_or_loss(current_stock_price)
-------------------------------------------------

Aufgabe:
Berechnet den aktuellen Gewinn oder Verlust der Aktien.

Parameter:
current_stock_price:
Aktueller Preis pro Aktie.

Formel:
Gewinn oder Verlust =
(aktueller Aktienpreis - Kaufpreis) × Aktienanzahl

Python:
(current_stock_price - purchase_price) * purchased_volume

Ergebnis:
Positiver Wert:
Gewinn

Negativer Wert:
Verlust

Wert 0:
Weder Gewinn noch Verlust

Beispiel:
Kaufpreis = 50 €
aktueller Preis = 60 €
Volumen = 10

Gewinn:
(60 - 50) × 10 = 100 €


4. FUNKTION: total_capital(current_stock_price)
------------------------------------------------

Aufgabe:
Berechnet das gesamte Vermögen.

Das Gesamtkapital besteht aus:
1. verfügbarem Kapital
2. gebundenem Kapital

Gebundenes Kapital:
Wert der aktuell gehaltenen Aktien.

Formel:
Gebundenes Kapital =
Aktienanzahl × aktueller Aktienpreis

Python:
purchased_volume * current_stock_price

Verfügbares Kapital:
Das noch vorhandene Bargeld.

Python:
capital

Gesamtkapital:
Gebundenes Kapital + verfügbares Kapital

Formel:
Gesamtkapital =
(purchased_volume × current_stock_price) + capital

Python:
purchased_volume * current_stock_price + capital


5. FUNKTION: purchase_sell(current_stock_price, volume)
--------------------------------------------------------

Aufgabe:
Kauft oder verkauft Aktien.

Parameter:
current_stock_price:
Aktueller Preis pro Aktie.

volume:
Anzahl der zu kaufenden oder zu verkaufenden Aktien.

volume > 0:
Aktien werden gekauft.

volume < 0:
Aktien werden verkauft.

volume == 0:
Keine Transaktion.


VORAUSSETZUNG FÜR KAUF UND VERKAUF

Das Aktiensymbol muss gültig sein.

Prüfung:
symbol.isalnum()

isalnum() bedeutet:
Das Symbol enthält nur Buchstaben und Zahlen.

Beispiele:
"AAPL"   -> True
"BMW123" -> True
"BMW.DE" -> False
""       -> False


KAUF

Ein positiver volume-Wert bedeutet Kauf.

Formel für die Kaufkosten:
Kaufkosten = aktueller Preis × gekauftes Volumen

Python:
purchase_cost = current_stock_price * volume

Bedingung:
Die Kaufkosten dürfen nicht größer als das verfügbare Kapital sein.

Prüfung:
purchase_cost <= capital

Nach erfolgreichem Kauf:

Neues Kapital:
capital = capital - purchase_cost

Neuer Aktienbestand:
purchased_volume = purchased_volume + volume

Neuer gespeicherter Kaufpreis:
purchase_price = current_stock_price

Beispiel:
Kapital = 1000 €
Preis = 50 €
Volumen = 4

Kaufkosten:
50 × 4 = 200 €

Neues Kapital:
1000 - 200 = 800 €

Neuer Aktienbestand:
0 + 4 = 4 Aktien


VERKAUF

Ein negativer volume-Wert bedeutet Verkauf.

Beispiel:
volume = -3

Das bedeutet:
3 Aktien verkaufen.

Bedingung:
Man darf nicht mehr Aktien verkaufen, als man besitzt.

Prüfung:
abs(volume) <= purchased_volume

Formel für den Verkaufserlös:
Verkaufserlös =
aktueller Preis × Anzahl der verkauften Aktien

Python:
sale_income = current_stock_price * abs(volume)

Neues Kapital:
capital = capital + sale_income

Neuer Aktienbestand:
purchased_volume = purchased_volume + volume

Warum wird addiert?
Weil volume negativ ist.

Beispiel:
purchased_volume = 10
volume = -3

10 + (-3) = 7 Aktien

Rückgabewert:
True:
Kauf oder Verkauf war erfolgreich.

False:
Symbol ungültig,
nicht genügend Kapital,
nicht genügend Aktien
oder volume ist 0.


6. FUNKTION: pretty_str(current_stock_price)
---------------------------------------------

Aufgabe:
Erstellt einen schönen und lesbaren Ausgabestring.

Parameter:
current_stock_price:
Aktueller Preis pro Aktie.

Bedingung:
Das Symbol muss ein String und alphanumerisch sein.

Prüfung:
isinstance(symbol, str) and symbol.isalnum()

Wenn kein gültiges Symbol gesetzt ist:
Rückgabe eines Leerstrings.

Python:
return ""

Wenn das Symbol gültig ist:
Die Funktion gibt folgende Informationen zurück:

1. Aktiensymbol
2. gekauftes Volumen
3. Gewinn oder Verlust
4. gebundenes Kapital
5. verfügbares Kapital
6. Gesamtkapital

Verwendete Formeln:

Gewinn oder Verlust:
(current_stock_price - purchase_price)
* purchased_volume

Gebundenes Kapital:
purchased_volume * current_stock_price

Verfügbares Kapital:
capital

Gesamtkapital:
(purchased_volume * current_stock_price)
+ capital

Wichtig:
pretty_str() verwendet return und nicht print.

return:
Gibt den String an den Aufrufer zurück.

print:
Zeigt einen Wert nur auf dem Bildschirm an.


KURZE FORMELÜBERSICHT
---------------------

Kaufkosten:
current_stock_price * volume

Verkaufserlös:
current_stock_price * abs(volume)

Gewinn oder Verlust:
(current_stock_price - purchase_price)
* purchased_volume

Gebundenes Kapital:
purchased_volume * current_stock_price

Verfügbares Kapital:
capital

Gesamtkapital:
purchased_volume * current_stock_price + capital

Kapitaländerung:
capital = capital + capital_change

Aktienbestand nach Kauf oder Verkauf:
purchased_volume = purchased_volume + volume
"""
