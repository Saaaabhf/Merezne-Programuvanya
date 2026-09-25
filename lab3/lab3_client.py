import requests # Бібліотека для відправки запитів

BASE_URL = 'http://127.0.0.1:8000/items'
# Дані для базової аутентифікації
AUTH = ('admin', '12345')

# 1. Отримуємо весь каталог
print("--- 1. Fetching the entire catalog (GET) ---")
response = requests.get(BASE_URL, auth=AUTH)
print(response.json())
print()

# 2. Створюємо новий товар
print("--- 2. Creating a new item (POST) ---")
new_product = {"name": "Keyboard", "price": 150, "color": "rgb"}
response = requests.post(BASE_URL, auth=AUTH, json=new_product)
print(response.json())
print()

# 3. Читаємо конкретний товар за ID = 1
print("--- 3. Fetching item with ID 1 (GET /items/1) ---")
response = requests.get(f"{BASE_URL}/1", auth=AUTH)
print(response.json())
print()

# 4. Оновлюємо товар (змінюємо тільки ціну)
print("--- 4. Updating item with ID 1 (PUT) ---")
update_data = {"price": 9999}
response = requests.put(f"{BASE_URL}/1", auth=AUTH, json=update_data)
print(response.json())
print()

# 5. Видаляємо товар під ID 2
print("--- 5. Deleting item with ID 2 (DELETE) ---")
response = requests.delete(f"{BASE_URL}/2", auth=AUTH)
print(response.json())
print()

# 6. Перевіряємо фінальний вигляд каталогу
print("--- 6. Final catalog check (GET) ---")
response = requests.get(BASE_URL, auth=AUTH)
print(response.json())
