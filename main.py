
import json

def run():
    while True:
        print("""0 - Kilépés
1 - Pénztáros mód
2 - Admin mód""")
        choice = int(input("Válasszon menüpontot: "))
        if choice == 0:
            break

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def list_guests(guests):
    for index, guest in enumerate(guests, start=1):
        print(f"{index} - {guest['name']}: {guest['balance']} Ft")

def list_drinks(drinks):
    for index, drink in enumerate(drinks, start=1):
        if drink['stock'] > 0:
            print(f"{index} - {drink['name']}: {drink['price']} Ft/{drink['unit']}")

def add_new_guest(guests):
    new_name = input("Adja meg az új törzsvendég nevét: ")
    for guest in guests:
        if guest['name'] == new_name:
            print("Hiba: Ez a név már létezik!")
            return
    guests.append({"name": new_name, "balance": 0})
    save_data(guests, "data/guests.json")

def make_order(guests, drinks):
    print("Válasszon vendéget:")
    list_guests(guests)
    guest_choice = int(input("Válasszon vendéget: ")) - 1

    if guest_choice < 0:
        return

    print("Válasszon italt:")
    list_drinks(drinks)
    drink_choice = int(input("Válasszon italt: ")) - 1

    if drink_choice < 0:
        return

    quantity = int(input("Mennyiség dl egységben: "))
    if quantity <= 0:
        print("Hiba: Nemnegatív egész számot adjon meg!")
        return

    selected_drink = drinks[drink_choice]
    if quantity * selected_drink['price'] > guests[guest_choice]['balance']:
        print("Hiba: Nincs elég készlet!")
        return

    guests[guest_choice]['balance'] -= quantity * selected_drink['price']
    selected_drink['stock'] -= quantity

    save_data(guests, "data/guests.json")
    save_data(drinks, "data/drinks.json")

    print(f"+{quantity * selected_drink['price']} Ft {guests[guest_choice]['name']} számlájára írva, egyenleg: {guests[guest_choice]['balance']} Ft")

def make_payment(guests):
    print("Válasszon vendéget:")
    list_guests(guests)
    guest_choice = int(input("Válasszon vendéget: ")) - 1

    if guest_choice < 0:
        return

    payment = int(input("Adja meg a befizetett pénzmennyiséget: "))
    guests[guest_choice]['balance'] += payment

    save_data(guests, "data/guests.json")

    print(f"{payment} Ft hozzáadva {guests[guest_choice]['name']} egyenlegéhez. Új egyenleg: {guests[guest_choice]['balance']} Ft")

def admin_mode(drinks):
    while True:
        print("0 - Vissza")
        for index, drink in enumerate(drinks, start=1):
            print(f"{index} - {drink['name']}: {drink['price']} Ft/{drink['unit']}")

        print("99 - Új ital hozzáadása")
        drink_choice = int(input("Válasszon italt: ")) - 1

        if drink_choice == -1:
            break
        elif drink_choice == 98:
            new_name = input("name: ")
            new_unit = input(f"unit[{drinks[0]['unit']}]: ") or drinks[0]['unit']
            new_price = int(input(f"price[{drinks[0]['price']}]: ") or drinks[0]['price'])
            new_stock = int(input(f"stock[{drinks[0]['stock']}]: ") or drinks[0]['stock'])
            drinks.append({"name": new_name, "unit": new_unit, "price": new_price, "stock": new_stock})
        else:
            drink = drinks[drink_choice]
            drink['name'] = input(f"name[{drink['name']}]: ") or drink['name']
            drink['unit'] = input(f"unit[{drink['unit']}]: ") or drink['unit']
            drink['price'] = int(input(f"price[{drink['price']}]: ") or drink['price'])
            drink['stock'] = int(input(f"stock[{drink['stock']}]: ") or drink['stock'])

        save_data(drinks, "data/drinks.json")

def run():
    guests = load_data("data/guests.json")
    drinks = load_data("data/drinks.json")

    while True:
        print("""0 - Kilépés
1 - Pénztáros mód
2 - Admin mód""")
        choice = int(input("Válasszon menüpontot: "))
        if choice == 0:
            break
        elif choice == 1:
            while True:
                print("""0 - Vissza a főmenübe
1 - Új törzsvendég
2 - Rendelés
3 - Befizetés""")
                option = int(input("Válasszon menüpontot: "))
                if option == 0:
                    break
                elif option == 1:
                    add_new_guest(guests)
                elif option == 2:
                    make_order(guests, drinks)
                elif option == 3:
                    make_payment(guests)
                else:
                    print("Hibás választás!")
        elif choice == 2:
            admin_mode(drinks)
        else:
            print("Hibás választás!")

if __name__ == "__main__":
    run()




