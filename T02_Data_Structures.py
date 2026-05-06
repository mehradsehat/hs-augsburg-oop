people = [
    {
        "surname": "Jan",
        "name": "Hofer",
        "plz": "42593",
        "place": "Altheim",
        "age": 12,
        "capital": 216.3,
        "hobbies": "Radfahren",
    },
    {
        "surname": "Maria",
        "name": "Becker",
        "plz": "16913",
        "place": "Berlin",
        "age": 25,
        "capital": 13235.23,
        "hobbies": "Tauchen",
    },
]

print(
    f"|{'Vorname':<15}|{'Name':<20}|{'PLZ':<7}|{'Ort':<10}|{'Alter':<5}|{'Vermögen':>12}|{'Hobbies':<15}|"
)
print("-" * 96)

for person in people:
    print(
        # har bar ye person az list gerefte mishe
        f"|{person['surname']:<15}"
        # surname ro chap mikone, ba arz 15 character, chap-chin (<)
        f"|{person['name']:<20}"
        # name ro ba arz 20 chap mikone
        f"|{person['plz']:<7}"
        # plz (code posti) ba arz 7
        f"|{person['place']:<10}"
        # shahr ba arz 10
        f"|{person['age']:<5}"
        # sen ba arz 5
        f"|{person['capital']:>12.2f}"
        # capital (pool) ro rast-chin (>) mikone
        # arz 12 dar nazar migire
        # .2f yani 2 ragham ashari (mesle 216.30)
        f"|{person['hobbies']:<15}|"
        # hobbies ba arz 15, chap-chin
        # | akhar baraye bastan jadval
    )
