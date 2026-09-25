import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Файли, де ми будемо зберігати наші дані
CATALOG_FILE = 'catalog.json'
USERS_FILE = 'users.json'

# Якщо файлу з користувачами немає, створюємо його з одним адміном
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({"admin": "12345"}, f)

# Якщо файлу з каталогом немає, створюємо його з тестовими товарами
if not os.path.exists(CATALOG_FILE):
    with open(CATALOG_FILE, 'w') as f:
        json.dump({
            "1": {"name": "Laptop", "price": 1000, "color": "black"},
            "2": {"name": "Mouse", "price": 50, "color": "white"}
        }, f)

# --- ДОПОМІЖНІ ФУНКЦІЇ ---

def is_authorized(auth):
    """Перевіряє логін та пароль (HTTP Basic Auth)"""
    if not auth or not auth.username or not auth.password:
        return False
        
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
        
    if auth.username in users and users[auth.username] == auth.password:
        return True
    return False

def read_catalog():
    """Читає словник з файлу"""
    with open(CATALOG_FILE, 'r') as f:
        return json.load(f)

def write_catalog(data):
    """Записує оновлений словник назад у файл"""
    with open(CATALOG_FILE, 'w') as f:
        json.dump(data, f, indent=4)



# Ендпоінт для всіх товарів. Дозволені методи GET (читати) та POST (створити)
@app.route('/items', methods=['GET', 'POST'])
def handle_items():
    # Захист: якщо пароль не підходить, віддаємо помилку англійською
    if not is_authorized(request.authorization):
        return jsonify({"error": "Unauthorized. Bad login or password"}), 401
    
    catalog = read_catalog()

    # Якщо запит GET - повертаємо весь каталог
    if request.method == 'GET':
        return jsonify(catalog)
    
    # Якщо запит POST - додаємо новий товар
    if request.method == 'POST':
        new_item = request.get_json()
        
        # Генеруємо новий ID
        if len(catalog) > 0:
            new_id = str(max([int(k) for k in catalog.keys()]) + 1)
        else:
            new_id = "1"
            
        catalog[new_id] = {
            "name": new_item.get("name", "Unknown"),
            "price": new_item.get("price", 0),
            "color": new_item.get("color", "Unknown")
        }
        write_catalog(catalog)
        
        return jsonify({"message": "Item created successfully", "id": new_id}), 201


# Ендпоінт для конкретного товару. Методи GET, PUT, DELETE
@app.route('/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_item(item_id):
    if not is_authorized(request.authorization):
        return jsonify({"error": "Unauthorized"}), 401
        
    catalog = read_catalog()
    
    # Якщо такого товару немає - віддаємо помилку
    if item_id not in catalog:
        return jsonify({"error": "Item not found"}), 404
        
    # Читаємо один товар за ID
    if request.method == 'GET':
        return jsonify(catalog[item_id])
        
    # Оновлюємо товар 
    if request.method == 'PUT':
        update_data = request.get_json()
        
        if "name" in update_data:
            catalog[item_id]["name"] = update_data["name"]
        if "price" in update_data:
            catalog[item_id]["price"] = update_data["price"]
        if "color" in update_data:
            catalog[item_id]["color"] = update_data["color"]
            
        write_catalog(catalog)
        return jsonify({"message": "Item updated successfully", "item": catalog[item_id]})
        
    # Видаляємо товар 
    if request.method == 'DELETE':
        del catalog[item_id]
        write_catalog(catalog)
        return jsonify({"message": "Item deleted successfully"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
