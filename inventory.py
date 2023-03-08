from tabulate import tabulate

LIGHT_RED = "\033[1;31m"
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
END = "\033[0m"


class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost/100

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country} {self.code} {self.product} {self.quantity}"


# An empty list is created to store a list of shoe 'objects'.
shoe_list = []

# ==========Functions outside the class==============


# The function below updates the inventory.txt file each time amendments are made:


def update():
    with open("inventory.txt", "w+") as file:
        file.write("Country,Code,Product,Cost,Quantity")
        for shoe_amendment in shoe_list:
            file.write(
                f"\n{shoe_amendment.country},{shoe_amendment.code},{shoe_amendment.product},{shoe_amendment.cost},{shoe_amendment.quantity}")

# The function below reads the inventory.txt file and adds each shoe stock entry to the shoe list.
# This function is called straight away when the program is run.


def read_shoes_data():
    try:
        with open("inventory.txt", "r") as inventory_file:
            next(inventory_file)  # skips first line of file
            inventory_data = inventory_file.readlines()
            for shoe_product in inventory_data:
                shoe_product_list = shoe_product.split(",")
                new_shoe = Shoe(shoe_product_list[0], shoe_product_list[1],
                                shoe_product_list[2], int(shoe_product_list[3]), int(shoe_product_list[4]))
                shoe_list.append(new_shoe)
    except FileNotFoundError:
        with open("inventory.txt", "w") as inventory_file:
            inventory_file.write("Country,Code,Product,Cost,Quantity")

# The two functions below allow the user to add a new shoe to the .txt file inventory.
# First function (input_checks()) uses defensive programming to ensure that user inputs are in correct format.
# Second function (capture_shoes()) stores the new shoe in the shoe list.


def input_checks():
    country = input(
        "\nWhat country is the shoe from? ").strip().title()
    while True:
        code = input("\nPlease enter shoe code starting SKU: ").upper()
        if code.startswith("SKU") == True and len(code) == 8:
            break
        else:
            print(
                f"{LIGHT_RED}Please start your code with SKU and then 5 numbers{END}")
    product = input("\nPlease enter product name: ").title()
    while True:
        try:
            cost = int(
                input("\nWhat is the cost of the shoe in pounds and pence? "))
            break
        except ValueError:
            print(
                f"{LIGHT_RED}Please enter a numerical cost in pounds and pence with no decimal point or currency character.{END}")
    while True:
        try:
            quantity = int(input("\nWhat is the stock quantity? "))
            break
        except ValueError:
            print(
                f"{LIGHT_RED}Please enter a number with no decimal point: {END}")
    capture_shoes(country, code, product, cost, quantity)
    print(f"{GREEN}New shoe successfully added to the inventory{END}")


def capture_shoes(country, code, product, cost, quantity):
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)
    update()

# The function below allows the user to view all shoes in the inventory in a table format:


def view_all():
    all_shoes = []
    if len(shoe_list) == 0:
        print(f"{LIGHT_RED}There are no shoes currently in the inventory. Please add to the inventory{END}.")
    else:
        for shoe in shoe_list:
            all_shoes.append(
                [shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity])
        print(tabulate(all_shoes, headers=[
            "Country", "Code", "Product", "Cost", "Quantity"], tablefmt="pretty"))

# The function below displays the shoe with the lowest stock and gives the user the option to add further stock.
# If they wish to add further stock, the number they wish to add is added to the quantity value.
# The update function is then called to rewrite the inventory in the .txt file.
# If the user does not wish to add further stock, they are taken back to the main menu.


def re_stock():
    try:
        min_shoe = min(shoe_list, key=lambda shoe: shoe.get_quantity())
        print("The shoe with the lowest stock quantity is:")
        output = f"{BLUE}==================="
        output += f"\nShoe Code: {min_shoe.code}:"
        output += f"\nName: {min_shoe.product}"
        output += f"\nCountry: {min_shoe.country}"
        output += "\nPrice: £"+"{:.2f}".format(min_shoe.get_cost())
        output += f"\nIn stock: {min_shoe.get_quantity()}"
        output += f"\n==================={END}"
        print(output)
        to_update = input(
            "Do you want to update the stock levels for this shoe? y/n ")
        if to_update.lower() == "y":
            shoes_to_add = int(
                input("How many more of these shoe would you like to add to the inventory? "))
            for shoe in shoe_list:
                if shoe.code == min_shoe.code:
                    shoe.quantity += shoes_to_add
            print(f"{GREEN}Shoe stock updated!{END}")
        else:
            print(f"{LIGHT_RED}Shoe stock not updated!{END}")
        update()
    except ValueError:
        print(f"{LIGHT_RED}There are no shoes currently in the inventory. Please add to the inventory{END}")

# The function below allows the user to search for a shoe with the shoe code.


def search_shoe():
    entered_shoe_code = input(
        "Please enter the shoe code: ").upper().strip()
    for shoe in shoe_list:
        if shoe.code == entered_shoe_code:
            output = f"{BLUE}{shoe.code}"
            output += f"\n====================="
            output += f"\nName: {shoe.product}"
            output += f"\nCountry: {shoe.country}"
            output += "\nPrice: £"+"{:.2f}".format(shoe.get_cost())
            output += f"\nIn stock: {shoe.get_quantity()}"
            output += f"\n====================={END}"
            print(output)
            break
    else:
        print(f"{LIGHT_RED}This shoe cannot be found in the inventory. Please try again or a new code{END}")

# The function below allows the user to see the total value of the stock for each shoe.


def value_per_item():
    if len(shoe_list) == 0:
        print(
            f"{LIGHT_RED}There are no shoes in the inventory. Please add to the inventory.{END}")
    else:
        for shoe in shoe_list:
            total_value = (float(shoe.get_cost())*int(shoe.get_quantity()))
            output = shoe.product+": £"+"{:.2f}".format(total_value)
            print(f"{BLUE}{output}{END}")

# The function below prints the shoe details for the shoe with the highest stock.


def highest_qty():
    try:
        max_quantity = max(shoe_list, key=lambda shoe: shoe.get_quantity())
        print("The shoe with the highest stock quantity is:")
        output = f"{BLUE}==================="
        output += f"\nShoe Code: {max_quantity.code}:"
        output += f"\nName: {max_quantity.product}"
        output += f"\nCountry: {max_quantity.country}"
        output += "\nPrice: £"+"{:.2f}".format(max_quantity.get_cost())
        output += f"\nIn stock: {max_quantity.get_quantity()}"
        output += f"\n==================={END}"
        print(output)
    except ValueError:
        print(f"{LIGHT_RED}There are no shoes currently in the inventory. Please add to the inventory.{END}")


# ==========Main Menu=============

welcome_menu = '''
Welcome to the shoe warehouse stock management system! What would you like to do?
=======================MENU==================================
A - add a new shoe to inventory
B-  view all shoes in stock
C - view lowest stocked shoe and restock
D - search shoe by code
E - view overall shoe values
F - view highest stocked shoe
Z - exit
=============================================================
'''
user_choice = ""
read_shoes_data()


while True:
    user_choice = input(welcome_menu).strip().lower()
    if user_choice == "a":
        input_checks()

    elif user_choice == "b":
        view_all()

    elif user_choice == "c":
        re_stock()

    elif user_choice == "d":
        search_shoe()

    elif user_choice == "e":
        value_per_item()

    elif user_choice == "f":
        highest_qty()

    elif user_choice == "z":
        print("Goodbye!")
        exit()

    else:
        print(f"{LIGHT_RED}You have not picked a valid option, try again{END}")
