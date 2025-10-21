import datetime
import json
import math

from app.car import Car
from app.shop import Shop
from app.customer import Customer


def shop_trip() -> None:
    customers = []
    shops = []
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    fuel_price = config["FUEL_PRICE"]

    for customer in config["customers"]:
        customers.append(Customer(
            name=customer["name"],
            product_cart=customer["product_cart"],
            location=customer["location"],
            money=customer["money"],
            car=Car(
                brand=customer["car"]["brand"],
                fuel_consumption=customer["car"]["fuel_consumption"]
            )
        ))

    for shop in config["shops"]:
        shops.append(Shop(
            name=shop["name"],
            location=shop["location"],
            products=shop["products"]
        ))

    for customer in customers:
        product_costs = []
        fuel_costs = []
        for shop in shops:
            dx = shop.location[0] - customer.location[0]
            dy = shop.location[1] - customer.location[1]
            distance = math.sqrt(dx ** 2 + dy ** 2) * 2

            fuel_needed = (customer.car.fuel_consumption / 100) * distance
            fuel_cost = fuel_needed * fuel_price
            fuel_costs.append(fuel_cost)

            total_products = sum(
                shop.products[product] * customer.product_cart[product]
                for product in customer.product_cart
            )
            product_costs.append(total_products)

        print(f"{customer.name} has {customer.money} dollars")
        total_cost = product_costs[0] + fuel_costs[0]
        chosen_shop = shops[0]
        for idx in range(len(shops)):
            if product_costs[idx] + fuel_costs[idx] < total_cost:
                total_cost = product_costs[idx] + fuel_costs[idx]
                chosen_shop = shops[idx]
            print(f"{customer.name}'s trip to the {shops[idx].name} "
                  f"costs{(product_costs[idx] + fuel_costs[idx]): .2f}")

        if customer.money < total_cost:
            print(f"{customer.name} doesn't have enough money"
                  f" to make a purchase in any shop")
            if customers.index(customer) + 1 != len(customers):
                print()
            continue

        print(f"{customer.name} rides to {chosen_shop.name}")
        home_location = customer.location
        customer.location = chosen_shop.location
        print()
        date_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Date: {date_now}")
        print(f"Thanks, {customer.name}, for your purchase!")
        print("You have bought:")
        for product in customer.product_cart:
            price = chosen_shop.products[product]
            amount = customer.product_cart[product]
            total = price * amount
            print(f"{customer.product_cart[product]} {product}s "
                  f"for{total: g} dollars")
        print(f"Total cost is {product_costs[shops.index(chosen_shop)]}"
              f" dollars")
        print("See you again!")
        print()
        customer.location = home_location
        print(f"{customer.name} rides home")
        customer.money -= total_cost
        print(f"{customer.name} now has{customer.money: .2f} dollars")
        if customers.index(customer) + 1 != len(customers):
            print()
