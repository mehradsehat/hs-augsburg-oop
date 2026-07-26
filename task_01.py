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
ÜBERSICHT DER FUNKTIONEN
مرور کلی تابع‌ها
=========================


GLOBALE VARIABLEN
متغیرهای سراسری
-----------------

name:
نام کامل سهم (Name der Aktie)
مثال:
"Apple"

symbol:
نماد کوتاه سهم (Aktiensymbol)
مثال:
"AAPL"

purchase_price:
قیمت خرید هر سهم (Kaufpreis pro Aktie)

purchased_volume:
تعداد سهم‌هایی که در حال حاضر داریم
(gekauftes Volumen / Aktienanzahl)

capital:
پول نقد قابل استفاده
(verfügbares Kapital)


1. set_stock(stock_name, stock_symbol)
=======================================

Aufgabe / وظیفه:
این تابع نام و نماد سهم را ذخیره می‌کند.

stock_name:
نام سهم به صورت String

stock_symbol:
نماد سهم به صورت String

شرط:
هر دو پارامتر باید از نوع str باشند.

Prüfung / بررسی:

isinstance(stock_name, str)

و:

isinstance(stock_symbol, str)

اگر هر دو String باشند:

name = stock_name
symbol = stock_symbol

Rückgabewert / مقدار بازگشتی:

True:
نام و نماد با موفقیت ذخیره شده‌اند.

False:
حداقل یکی از پارامترها String نیست.


2. change_available_capital(capital_change)
============================================

Aufgabe / وظیفه:
این تابع سرمایه قابل استفاده
(verfügbares Kapital)
را افزایش یا کاهش می‌دهد.

capital_change > 0:
سرمایه افزایش پیدا می‌کند.

capital_change < 0:
سرمایه کاهش پیدا می‌کند.

capital_change == 0:
سرمایه تغییر نمی‌کند.

Formel / فرمول:

Neues Kapital =
altes Kapital + Kapitaländerung

سرمایه جدید =
سرمایه قبلی + مقدار تغییر سرمایه

Python:

capital = capital + capital_change

شرط مهم:
سرمایه نباید منفی شود.

Prüfung / بررسی:

abs(capital_change) <= capital

یا:

capital + capital_change >= 0

Rückgabewert:

True:
تغییر سرمایه با موفقیت انجام شده است.

False:
این تغییر باعث منفی شدن سرمایه می‌شود.


3. profit_or_loss(current_stock_price)
=======================================

Aufgabe / وظیفه:
این تابع سود یا ضرر فعلی
(Gewinn oder Verlust)
را محاسبه می‌کند.

current_stock_price:
قیمت فعلی هر سهم
(aktueller Aktienpreis)

Formel / فرمول:

Gewinn oder Verlust =
(aktueller Aktienpreis - Kaufpreis)
× Aktienanzahl

سود یا ضرر =
(قیمت فعلی - قیمت خرید)
× تعداد سهام

Python:

(current_stock_price - purchase_price)
* purchased_volume

Ergebnis / نتیجه:

مقدار مثبت:
Gewinn = سود

مقدار منفی:
Verlust = ضرر

مقدار صفر:
نه سود و نه ضرر

Beispiel / مثال:

purchase_price = 50
current_stock_price = 60
purchased_volume = 10

Gewinn:

(60 - 50) * 10 = 100 Euro


4. total_capital(current_stock_price)
======================================

Aufgabe / وظیفه:
این تابع کل سرمایه
(Gesamtkapital)
را محاسبه می‌کند.

Gesamtkapital شامل دو بخش است:

1. Gebundenes Kapital
سرمایه‌ای که داخل سهام قرار دارد.

2. Verfügbares Kapital
پول نقدی که هنوز قابل استفاده است.


Gebundenes Kapital
سرمایه درگیر در سهام:

Formel:

Gebundenes Kapital =
Aktienanzahl × aktueller Aktienpreis

سرمایه درگیر =
تعداد سهم × قیمت فعلی هر سهم

Python:

purchased_volume * current_stock_price


Verfügbares Kapital
سرمایه قابل استفاده:

این همان متغیر capital است.

Python:

capital


Gesamtkapital
کل سرمایه:

Formel:

Gesamtkapital =
gebundenes Kapital + verfügbares Kapital

کل سرمایه =
سرمایه درگیر + سرمایه قابل استفاده

Python:

purchased_volume * current_stock_price + capital


5. purchase_sell(current_stock_price, volume)
==============================================

Aufgabe / وظیفه:
این تابع سهم را می‌خرد یا می‌فروشد.

current_stock_price:
قیمت فعلی هر سهم
(aktueller Aktienpreis)

volume:
تعداد سهم مورد معامله
(gekauftes oder verkauftes Volumen)


volume > 0:
Kaufen = خرید

volume < 0:
Verkaufen = فروش

volume == 0:
هیچ معامله‌ای انجام نمی‌شود.


VORAUSSETZUNG
شرط اولیه معامله
----------------

نماد سهم باید معتبر باشد.

Prüfung:

symbol.isalnum()

isalnum() بررسی می‌کند که String فقط شامل
حروف و عدد باشد.

Beispiele:

"AAPL"   -> True
"BMW123" -> True
"BMW.DE" -> False
"AAPL!"  -> False
""       -> False


KAUFEN
خرید
------

اگر volume مثبت باشد، خرید انجام می‌شود.

مثال:

volume = 5

یعنی:
۵ سهم خریداری شود.

Kaufkosten / هزینه خرید:

Formel:

Kaufkosten =
aktueller Aktienpreis × gekauftes Volumen

هزینه خرید =
قیمت فعلی هر سهم × تعداد سهم خریداری‌شده

Python:

purchase_cost = current_stock_price * volume

شرط خرید:

purchase_cost <= capital

یعنی هزینه خرید نباید بیشتر از سرمایه قابل استفاده باشد.


Nach dem Kauf
بعد از خرید:

Kapital reduzieren
سرمایه کم می‌شود:

capital = capital - purchase_cost

Aktienbestand erhöhen
تعداد سهم افزایش پیدا می‌کند:

purchased_volume = purchased_volume + volume

Kaufpreis speichern
قیمت خرید جدید ذخیره می‌شود:

purchase_price = current_stock_price


Beispiel:

capital = 1000
current_stock_price = 50
volume = 4

Kaufkosten:

50 * 4 = 200

Neues Kapital:

1000 - 200 = 800

Neues Volumen:

0 + 4 = 4 Aktien


VERKAUFEN
فروش
--------

اگر volume منفی باشد، فروش انجام می‌شود.

مثال:

volume = -3

یعنی:
۳ سهم فروخته شود.

شرط فروش:

نباید بیشتر از تعداد سهامی که داریم بفروشیم.

Prüfung:

abs(volume) <= purchased_volume

abs(volume):
علامت منفی را حذف می‌کند.

مثال:

abs(-3) = 3


Verkaufserlös / درآمد فروش:

Formel:

Verkaufserlös =
aktueller Aktienpreis × verkauftes Volumen

درآمد فروش =
قیمت فعلی × تعداد سهم فروخته‌شده

Python:

sale_income = current_stock_price * abs(volume)


Kapital erhöhen
سرمایه افزایش پیدا می‌کند:

capital = capital + sale_income


Aktienbestand reduzieren
تعداد سهم کاهش پیدا می‌کند:

purchased_volume = purchased_volume + volume

چرا جمع می‌کنیم؟

چون volume منفی است.

مثال:

purchased_volume = 10
volume = -3

10 + (-3) = 7


Rückgabewert:

True:
خرید یا فروش موفق بوده است.

False:
یکی از شرایط زیر برقرار بوده است:

- Symbol معتبر نیست.
- سرمایه کافی نیست.
- تعداد سهم کافی نیست.
- volume برابر صفر است.


6. pretty_str(current_stock_price)
===================================

Aufgabe / وظیفه:
این تابع یک خروجی زیبا و خوانا
(schöne und lesbare Ausgabe)
ایجاد می‌کند.

current_stock_price:
قیمت فعلی هر سهم

شرط:

symbol باید:

1. از نوع String باشد.
2. فقط شامل حروف و اعداد باشد.

Prüfung:

isinstance(symbol, str)
and
symbol.isalnum()

اگر Symbol معتبر نباشد:

return ""

یعنی یک Leerstring
یا رشته خالی برگردانده می‌شود.


اگر Symbol معتبر باشد، اطلاعات زیر نمایش داده می‌شوند:

Aktiensymbol:
نماد سهم

Gekauftes Volumen:
تعداد سهام موجود

Gewinn/Verlust:
سود یا ضرر فعلی

Gebundenes Kapital:
سرمایه‌ای که در سهام قرار دارد

Verfügbares Kapital:
پول نقد قابل استفاده

Gesamtkapital:
کل دارایی


Verwendete Formeln
فرمول‌های استفاده‌شده
---------------------

Gewinn oder Verlust:

(current_stock_price - purchase_price)
* purchased_volume


Gebundenes Kapital:

purchased_volume * current_stock_price


Verfügbares Kapital:

capital


Gesamtkapital:

purchased_volume * current_stock_price + capital


WICHTIG
نکته مهم
---------

pretty_str() باید از return استفاده کند،
نه print.

return:
مقدار را از تابع برمی‌گرداند.

print:
فقط مقدار را روی صفحه نمایش می‌دهد.


KURZE FORMELÜBERSICHT
خلاصه فرمول‌ها
=====================

Kaufkosten
هزینه خرید:

current_stock_price * volume


Verkaufserlös
درآمد فروش:

current_stock_price * abs(volume)


Gewinn oder Verlust
سود یا ضرر:

(current_stock_price - purchase_price)
* purchased_volume


Gebundenes Kapital
سرمایه داخل سهام:

purchased_volume * current_stock_price


Verfügbares Kapital
سرمایه قابل استفاده:

capital


Gesamtkapital
کل سرمایه:

purchased_volume * current_stock_price + capital


Kapitaländerung
تغییر سرمایه:

capital = capital + capital_change


Aktienbestand nach Kauf oder Verkauf
تعداد سهم بعد از خرید یا فروش:

purchased_volume = purchased_volume + volume
"""
