# Unit-тести для програми catalog.py
# Запуск:          pytest
# Покриття:        pytest --cov=catalog
# HTML-звіт:       pytest --cov=catalog --cov-report html
import pytest
from catalog import Catalog


# Фікстура - перед кожним тестом створює каталог з двома товарами
@pytest.fixture
def catalog():
    c = Catalog()
    c.add_item("Laptop", 1000, "black")
    c.add_item("Mouse", 50, "white")
    return c


# --- Тести для __init__ ---

def test_init_empty_catalog():
    # Новий каталог має бути порожнім
    c = Catalog()
    assert c.items == {}


def test_init_separate_objects():
    # Два різні каталоги не повинні мати спільних даних
    c1 = Catalog()
    c2 = Catalog()
    c1.add_item("Laptop", 1000)
    assert c2.items == {}


# --- Тести для add_item ---

def test_add_item_first_id():
    # Перший товар отримує ID "1", колір за замовчуванням Unknown
    c = Catalog()
    new_id = c.add_item("Keyboard", 150)
    assert new_id == "1"
    assert c.items["1"] == {"name": "Keyboard", "price": 150, "color": "Unknown"}


def test_add_item_next_id(catalog):
    # Наступний ID = максимальний + 1
    new_id = catalog.add_item("Keyboard", 150, "rgb")
    assert new_id == "3"
    assert len(catalog.items) == 3


def test_add_item_empty_name():
    # Порожня назва - помилка
    c = Catalog()
    with pytest.raises(ValueError):
        c.add_item("", 100)


def test_add_item_negative_price():
    # Від'ємна ціна - помилка
    c = Catalog()
    with pytest.raises(ValueError):
        c.add_item("Monitor", -5)


# --- Тести для get_item ---

def test_get_item_exists(catalog):
    item = catalog.get_item("1")
    assert item["name"] == "Laptop"


def test_get_item_int_id(catalog):
    # ID можна передати і числом
    item = catalog.get_item(2)
    assert item["name"] == "Mouse"


def test_get_item_not_found(catalog):
    assert catalog.get_item("99") is None


# --- Тести для update_item ---

def test_update_item_price(catalog):
    # Змінюємо тільки ціну, інші поля не змінюються
    item = catalog.update_item("1", price=9999)
    assert item["price"] == 9999
    assert item["name"] == "Laptop"
    assert item["color"] == "black"


def test_update_item_all_fields(catalog):
    item = catalog.update_item(2, name="Gaming Mouse", price=80, color="red")
    assert item == {"name": "Gaming Mouse", "price": 80, "color": "red"}


def test_update_item_ignores_unknown_fields(catalog):
    # Зайві поля не додаються до товару
    item = catalog.update_item("1", weight=2)
    assert "weight" not in item


def test_update_item_not_found(catalog):
    with pytest.raises(KeyError):
        catalog.update_item("99", price=10)


def test_update_item_negative_price(catalog):
    with pytest.raises(ValueError):
        catalog.update_item("1", price=-1)


# --- Тести для delete_item ---

def test_delete_item_exists(catalog):
    assert catalog.delete_item("2") is True
    assert catalog.get_item("2") is None
    assert len(catalog.items) == 1


def test_delete_item_not_found(catalog):
    # Неіснуючий товар - повертається False, каталог не змінюється
    assert catalog.delete_item("99") is False
    assert len(catalog.items) == 2


# --- Тести для total_price ---

def test_total_price(catalog):
    assert catalog.total_price() == 1050


def test_total_price_empty():
    c = Catalog()
    assert c.total_price() == 0


# --- Тести для find_by_color ---

def test_find_by_color(catalog):
    catalog.add_item("Monitor", 300, "black")
    assert catalog.find_by_color("black") == ["Laptop", "Monitor"]


def test_find_by_color_case_insensitive(catalog):
    assert catalog.find_by_color("WHITE") == ["Mouse"]


def test_find_by_color_not_found(catalog):
    assert catalog.find_by_color("green") == []


# --- Тести для save_to_file / load_from_file ---
# tmp_path - вбудована фікстура pytest, дає тимчасову папку для файлів

def test_save_and_load(catalog, tmp_path):
    # Зберігаємо, завантажуємо в новий каталог - дані мають співпасти
    file = tmp_path / "catalog.json"
    catalog.save_to_file(file)

    new_catalog = Catalog()
    new_catalog.load_from_file(file)
    assert new_catalog.items == catalog.items


def test_save_creates_file(catalog, tmp_path):
    file = tmp_path / "catalog.json"
    catalog.save_to_file(file)
    assert file.exists()


def test_load_replaces_old_data(catalog, tmp_path):
    # Після завантаження старі товари зникають
    file = tmp_path / "catalog.json"
    file.write_text('{"1": {"name": "Phone", "price": 500, "color": "blue"}}')
    catalog.load_from_file(file)
    assert catalog.items == {"1": {"name": "Phone", "price": 500, "color": "blue"}}


def test_load_file_not_found(tmp_path):
    c = Catalog()
    with pytest.raises(FileNotFoundError):
        c.load_from_file(tmp_path / "no_file.json")
