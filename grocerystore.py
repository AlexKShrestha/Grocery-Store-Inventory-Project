import sys
import random
import pandas as pd
import matplotlib.pyplot as plt

class Product:
    """
    A class that represents a product in a grocery store.

    Attributes:
    - name (str): the name of the product
    - price (float): the price of the product
    - quantity (int): the quantity of the product in the store

    Methods:
    - __init__(self, name, price, quantity): Initializes a product with its name, price, and quantity.
    - get_name(self): Returns the name of the product.
    - get_price(self): Returns the price of the product.
    - get_quantity(self): Returns the quantity of the product in the store.
    - set_price(self, new_price): Sets a new price for the product.
    - set_quantity(self, new_quantity): Sets a new quantity for the product in the store.
    """
    def __init__(self, name, category, quantity, price):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        
    def get_category(self):
        return self.category

    def get_name(self):
        return self.name
    
    def get_quantity(self):
        return self.quantity
    
    def __repr__(self):
        return f'(Item: {self.name}, Category: {self.category}, Quantity = {self.quantity}, Price = ${self.price})'
    
    
class GroceryStore:
    """
    A class that represents a grocery store.

    Attributes:
    - name (str): the name of the grocery store
    - inventory (dict): a dictionary of product names and their quantities in the store

    Methods:
    - __init__(self, name, inventory): Initializes a grocery store with the name of it and its inventory.
    - setup_store(self, stock): Populates the inventory of the grocery store with products and their quantities 
                                from a file named "stock". 
    """
    def __init__(self, name = "", inventory = "grocery store inventory.csv"):
        """Intializes a grocery store and creates its inventory from a csv file.
        
        Args:
            name (str): a phone number given as a str or int
            inventory (str): a str containing the name of the csv file
        Side effects:
            Sets attributes
        """
        self.name = name
        self.inventory = dict()
        with open(inventory, "r", encoding="utf-8") as f:
            next(f)
            for line in f:
                item, category, quantity, price = line.strip().split(',')
                self.inventory[item] = Product(item, category, int(quantity), int(price))

    def get_inventory(self):
        return self.inventory
    
class Shopper: 
    """
    A class that represents a shopper.

    Attributes:
    - cart (list): a list of items in the shopper's cart
    - budget (float): the amount of money the shopper has to spend
    - store_prices (dict): a dictionary of product names and their prices in the grocery store

    Methods:
    - __init__(self, budget, store_prices): Initializes a shopper with a budget and the prices of products 
                                             in the grocery store.
    - add(self, item, price, inventory): Adds an item to the shopper's cart if it is available in the inventory 
                                         and the shopper's budget is sufficient to buy it.
    - checkout(self): Calculates the total cost of items in the shopper's cart and returns it. 
                      The cart is then cleared.
    """
    def __init__(self, name, budget):
        self.name = name
        self.cart = {}
        self.budget = budget
        self.coupon = None

    def add(self, product_name, quantity, store):
        if product_name not in store.inventory:
            print(f"Sorry! We dont have {product_name}")
            return
        product = store.inventory[product_name]
        total_price = product.price * quantity
        if total_price + sum([store.inventory[p].price * self.cart[p] for p in self.cart]) > self.budget:
            print(f"Item cost to much, put it back!")
            return
        if product_name in self.cart:
            self.cart[product_name] += quantity
        else:
            self.cart[product_name] = quantity
        df.loc[product_name, "Quantity"] = (store.inventory[product_name].get_quantity() - quantity)
        print(f"{quantity} {product_name} added to your cart.")
    
    def generate_coupon(self):
    # method that will generate a random discount (int between 5, 20)
    # and choose a random product and print the resulting information
        product_name = random.choice(list(self.cart.keys()))
        discount = random.randint(5, 20)
        coupon = Coupon(discount, product_name)
        print(f"You received a {discount}% discount on {product_name}")

        return coupon
    
    def checkout(self, store):
        total_price = 0
        for product_name, quantity in self.cart.items():
            product = store.inventory[product_name]
            total_price += product.price * quantity
        if self.coupon:
            discount = self.coupon.discount
            total_price *= (1 - (discount/100))
        print(f"Your total price comes to: ${round(total_price, 2)}")
        return total_price

class Coupon:
    """
    A class that represents a coupon for a shopper. Ues conditional expression and set operations.

    Attributes:
    - discount (int): the randomly generated discount for the coupon
    - product_name (str): the name of the product the coupon is for

    Methods:
    - __init__(self): Initializes the discount and product name of the coupon
    - get_discount(self, product_name): Returns the discount for a specific product in the shopper's coupons.
    
    """
    def __init__(self, discount, product_name): 
        self.discount = discount
        self.product_name = product_name
    
    def get_discount(self):
        return self.discount
    
    def __repr__(self):
        return f'Coupon: {self.discount}% off {self.product_name}'


if __name__ == '__main__':
    store_name = input("Welcome! What grocery store would you like to shop at today? ")
    store = GroceryStore(store_name,)
    
    shopper_name = input(f"Thanks for choosing {store_name}! What's your name? ")
    budget = float(input(f"{shopper_name}, What's your budget for today? $"))

    shopper = Shopper(shopper_name, budget)
    df = pd.read_csv("grocery store inventory.csv", index_col="Item")
    
    while True:
        choice = input("Would you like to add an item to your cart, checkout, or leave? ").lower()
        if choice == "add":
            print(df)
            item_name = input("What would you like to add to your cart? ")
            quantity = int(input(f"How many {item_name} would you like to add to your cart? "))
            shopper.add(item_name, quantity, store)
        elif choice == "checkout":
            if not shopper.cart:
                print("Your cart is empty!")
                continue
            shopper.coupon = shopper.generate_coupon()
            coupon_choice = input("Would you like to use a coupon? ").lower()
            if coupon_choice == "yes":
                shopper.checkout(store)
                print("Have a nice day!")

                break
            elif coupon_choice == "no":
                print("Ok! Keep Shopping!")
        elif choice == "leave":
            print ("Come back again!")
            break
    
    #Show a bar graph of the previous inventory
    dfbefore = pd.read_csv("before inventory.csv")
    name = dfbefore['Item']
    quantity = dfbefore['Quantity']
    # Figure Size
    plt.barh(name, quantity, color = "red")
    plt.ylabel("Food Items")
    plt.xlabel("Quantity")
    plt.title("Previous Store Inventory")
    plt.show()
    
    #Show a bar graph of the current inventory
    df = df.reset_index()
    name = df['Item']
    quantity = df['Quantity']
    # Figure Size
    plt.barh(name, quantity)
    plt.ylabel("Food Items")
    plt.xlabel("Quantity")
    plt.title("Current Store Inventory")
    plt.show()