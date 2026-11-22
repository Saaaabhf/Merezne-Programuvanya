# Програма для тестування: каталог товарів у вигляді класу (ООП)
# Ідея та сама, що й у lab3 (товари з name, price, color), тільки без сервера
import json  # Для збереження та завантаження каталогу з файлу


class Catalog:
    """Клас каталогу товарів. Товари зберігаються у словнику {id: {name, price, color}}"""

    def __init__(self):
        # Порожній словник, куди будемо складати товари
        self.items = {}

    def add_item(self, name, price, color="Unknown"):
        """Додає новий товар і повертає його ID"""
        # Перевіряємо, що назва не порожня
        if not name:
            raise ValueError("Name cannot be empty")
        # Ціна не може бути від'ємною
        if price < 0:
            raise ValueError("Price cannot be negative")

        # Генеруємо новий ID так само, як у lab3 (максимальний + 1)
        if len(self.items) > 0:
            new_id = str(max([int(k) for k in self.items.keys()]) + 1)
        else:
            new_id = "1"

        self.items[new_id] = {"name": name, "price": price, "color": color}
        return new_id

    def get_item(self, item_id):
        """Повертає товар за ID, або None якщо такого немає"""
        return self.items.get(str(item_id))

    def update_item(self, item_id, **update_data):
        """Оновлює поля товару (name, price, color). Повертає оновлений товар"""
        item_id = str(item_id)

        # Якщо такого товару немає - кидаємо помилку
        if item_id not in self.items:
            raise KeyError("Item not found")

        # Нову ціну теж перевіряємо
        if "price" in update_data and update_data["price"] < 0:
            raise ValueError("Price cannot be negative")

        # Оновлюємо тільки ті поля, які дозволені
        for key in ["name", "price", "color"]:
            if key in update_data:
                self.items[item_id][key] = update_data[key]

        return self.items[item_id]

    def delete_item(self, item_id):
        """Видаляє товар за ID. Повертає True якщо видалили, False якщо не знайшли"""
        item_id = str(item_id)
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False

    def total_price(self):
        """Рахує загальну вартість усіх товарів у каталозі"""
        return sum(item["price"] for item in self.items.values())

    def find_by_color(self, color):
        """Повертає список назв товарів потрібного кольору (без різниці великі чи малі літери)"""
        return [item["name"] for item in self.items.values()
                if item["color"].lower() == color.lower()]

    def save_to_file(self, filename):
        """Записує каталог у JSON-файл"""
        with open(filename, 'w') as f:
            json.dump(self.items, f, indent=4)

    def load_from_file(self, filename):
        """Читає каталог з JSON-файлу (старі дані замінюються)"""
        with open(filename, 'r') as f:
            self.items = json.load(f)


# Невелика демонстрація роботи, якщо запускати файл напряму
if __name__ == "__main__":
    catalog = Catalog()
    catalog.add_item("Laptop", 1000, "black")
    catalog.add_item("Mouse", 50, "white")
    print(catalog.items)
    print(f"Total price: {catalog.total_price()}")
