from pydantic import BaseModel
from model import Product
import sqlite3

DB_FILE = 'milkis.db'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

#initializing a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price UNIQUE REAL NOT NULL,
        product_company TEXT DEFAULT NULL,
        quantity INTEGER DEFAULT 0
    )
''')
conn.commit()


def create_product(product: Product):
    cursor.execute('''
        INSERT INTO products (product_name, price, product_company, quantity)
        VALUES (?, ?, ?, ?)
    ''', (product.product_name, product.price, product.product_company, product.quantity))
    conn.commit()

def get_products():
    cursor.execute('SELECT id, product_name, price, product_company, quantity FROM products')
    products = cursor.fetchall()
    return products

def get_product(product_id: int):
    cursor.execute('SELECT product_name, price FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    return product

def update_product(product_id: int, product: Product):
    cursor.execute('''
        UPDATE products
        SET product_name = ?, price = ?
        WHERE id = ?
    ''', (product.product_name, product.price, product_id))
    conn.commit()
    return product

def add_quantity(item_name: str, quantity_to_add: int = 1):
    cursor.execute("UPDATE Products SET quantity = quantity + ? WHERE product_name = ?", (quantity_to_add, item_name))
    conn.commit()
    return True

def delete_productID(product_id: int):
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    return {"message": "Product deleted"}

def delete_productname(product_name: str):
    cursor.execute('DELETE FROM products WHERE product_name = ?', (product_name))
    conn.commit()
    return {"message": "Product deleted"}

def shutdown_event():
    conn.close()

#noah = Product.create_basic(product_name = "noah", price = 0.99)
#candy = Product.create_basic(product_name = "candy", price = 2.0)
#amazon = Product.create_basic(product_name = "amazon", price = 6969696969)

#create_product(candy)
#create_product(amazon)
#create_product(noah)

add_quantity('noah', 2)

product_list = get_products()

print(product_list)

shutdown_event()


