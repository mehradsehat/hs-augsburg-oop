people = []


def add_person():
    firstname = input("FirstName: ")
    lastname = input("LastName: ")
    plz = input("PLZ: ")
    city = input("City: ")
    age = int(input("Age: "))

    person = {
        "firstname": firstname,
        "lastname": lastname,
        "plz": plz,
        "city": city,
        "age": age,
    }


return add_person
