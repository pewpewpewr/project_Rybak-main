from datetime import datetime
import random

class User:
    def __init__(self, name, email, payment_info):
        self.name = name
        self.email = email
        self.payment_info = payment_info
        self.history = []

    def make_order(self, start_location, end_location, drivers):
        distance = random.randint(1, 14)  # Рандомайзер відстані між локаціями
        print(f"Відстань між {start_location} і {end_location} складає {distance} км.")
        
        print("Список доступних водіїв:")
        affordable_drivers = []
        for idx, driver in enumerate(drivers, 1):
            cost_estimate = driver.rate_per_km * distance
            if cost_estimate <= self.payment_info:
                affordable_drivers.append(driver)
                print(f"{idx}. {driver.name} - {driver.vehicle} (Рейтинг: {driver.rating}, Вартість за км: {driver.rate_per_km}грн, Всього: {cost_estimate}грн)")

        if not affordable_drivers:
            print("У вас недостатньо коштів. Поповніть баланс або виберіть іншого водія.")
            return None

        choice = int(input("Виберіть номер водія: ")) - 1
        if 0 <= choice < len(affordable_drivers):
            order = Order(start_location, end_location, self)
            affordable_drivers[choice].accept_order(order)
            self.history.append(order)
            return order
        else:
            print("Невірний вибір водія.")
            return None

    def display_history(self):
        if not self.history:
            print("Історія замовлень порожня.")
        else:
            for order in self.history:
                print(f"З {order.start_location} до {order.end_location} від {order.time.strftime('%Y-%m-%d %H:%M')} статус: {order.status}")

class Driver:
    def __init__(self, name, vehicle, rating, rate_per_km):
        self.name = name
        self.vehicle = vehicle
        self.rating = rating
        self.rate_per_km = rate_per_km
        self.history = []

    def accept_order(self, order):
        order.assign_driver(self)
        self.history.append(order)
        return "Замовлення прийнято."

    def display_history(self):
        if not self.history:
            print("Історія замовлень порожня.")
        else:
            for order in self.history:
                print(f"З {order.start_location} до {order.end_location} для {order.user.name} від {order.time.strftime('%Y-%m-%d %H:%M')} статус: {order.status}")

class Order:
    def __init__(self, start_location, end_location, user):
        self.start_location = start_location
        self.end_location = end_location
        self.user = user
        self.driver = None
        self.status = "В очікуванні"
        self.time = datetime.now()

    def assign_driver(self, driver):
        self.driver = driver
        self.status = "Призначений"

    def complete(self, cost):
        self.cost = cost
        self.status = "Виконано"
        self.time_completed = datetime.now()

def main():
    drivers = [
        Driver("Іван", "Toyota Corolla", 4.8, 10),
        Driver("Мухамед", "Honda Civic", 4.7, 12),
        Driver("Макс", "Ford Focus", 4.5, 9),
        Driver("Андрій", "Chevrolet Cruze", 4.6, 11),
        Driver("Аня", "Volkswagen Golf", 4.9, 13)
    ]

    print("Ласкаво просимо до системи замовлення таксі!")
    user_name = input("Введіть своє ім'я: ")
    user_email = input("Введіть свій email: ")
    user_payment_info = float(input("Введіть ваш баланс: "))  # Переводимо у тип float

    user = User(user_name, user_email, user_payment_info)

    while True:
        print("\n1. Зробіть нове замовлення таксі")
        print("2. Додати нового водія")
        print("3. Переглянути історію замовлень")
        print("4. Вихід")
        choice = input("Введіть свій вибір: ")

        if choice == "1":
            start_location = input("Введіть місце початку: ")
            end_location = input("Введіть кінцеве місце: ")
            order = user.make_order(start_location, end_location, drivers)
            if order:
                print("Замовлення таксі виконано успішно.")
                print("Статус:", order.status)
            else:
                print("Не вдалося створити замовлення.")

        elif choice == "2":
            name = input("Введіть ім'я водія: ")
            vehicle = input("Введіть марку та модель автомобіля: ")
            rating = float(input("Введіть рейтинг водія: "))
            rate_per_km = float(input("Введіть вартість за км: "))
            drivers.append(Driver(name, vehicle, rating, rate_per_km))
            print("Водій успішно доданий.")

        elif choice == "3":
            print("\nІсторія замовлень користувача:")
            user.display_history()

        elif choice == "4":
            print("Дякуємо за використання системи замовлення таксі!")
            break
        else:
            print("Невірний вибір. Будь ласка, спробуйте ще раз.")

if __name__ == "__main__":
    main()
