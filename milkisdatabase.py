"""
MILKIS VENDING MACHINE DATABASE INTERACTION CODE

1. Create the database with four tables: Inventory, Order history, vending machines
"""

from pydantic import BaseModel
from model import Item
import sqlite3
from prettytable import PrettyTable
import json

DB_FILE = 'milkis.db'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

#Creating the inventory table in the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL,
        item_company TEXT DEFAULT NULL,
        quantity INTEGER DEFAULT 0
    )
''')

#Creating the Order History table in the database
cursor.execute('''
CREATE TABLE IF NOT EXISTS orderhistory (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cost REAL NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES inventory(id)
)
''')

conn.commit()

###INVENTORY TABLE OPERATIONS###
def create_item(item: Item):
    #Creates a new unique item in the database

    cursor.execute('''
        INSERT INTO inventory (item_name, price, item_company, quantity)
        VALUES (?, ?, ?, ?)
    ''', (item.item_name, item.price, item.item_company, item.quantity))
    conn.commit()

def get_items():
    #Returns a list of all items in the database

    cursor.execute('SELECT id, item_name, price, item_company, quantity FROM inventory')
    items = cursor.fetchall()
    return items

def get_item(item_id: int):
    #Function to return a single item with the item_id identifier

    cursor.execute('SELECT item_name, price FROM inventory WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    return item

def update_item(item_id: int, item: Item):
    #Pass a new item object to update the item at the location of the item id in the database

    cursor.execute('''
        UPDATE inventory
        SET item_name = ?, price = ?
        WHERE id = ?
    ''', (item.item_name, item.price, item_id))
    conn.commit()
    return item

def add_quantity(item_name: str, quantity_to_add: int = 1):
    #modify the item in the database to add some integer quantity
    #wil mainly be used when putting in orders

    cursor.execute("UPDATE inventory SET quantity = quantity + ? WHERE item_name = ?", (quantity_to_add, item_name))
    conn.commit()
    return True

def delete_itemID(item_id: int):
    #Delete a item by ID from the database

    cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    return {"message": "Item deleted"}

def delete_itemname(item_name: str):
    # Check if the item exists in the database
    cursor.execute('SELECT COUNT(*) FROM inventory WHERE item_name = ?', (item_name,))
    count = cursor.fetchone()[0]

    if count == 0:
        return {"message": "Item not found"}

    # Delete the item from the database
    cursor.execute('DELETE FROM inventory WHERE item_name = ?', (item_name,))
    conn.commit()
    
    return {"message": "Item deleted"}

def display_inventory_table():
    # Display the entire inventory as a table

    try:
        # Execute a SELECT query to retrieve all entries from the inventory table
        cursor.execute('SELECT * FROM inventory')
        items = cursor.fetchall()

        if not items:
            return {"message": "No items found in the inventory"}

        # Create a PrettyTable to display the inventory
        table = PrettyTable()
        table.field_names = ["ID", "Item Name", "Price", "Item Company", "Quantity"]

        for item in items:
            table.add_row(item)

        return {"message": "Inventory:", "table": table.get_string()}

    except sqlite3.Error as e:
        return {"message": f"Error: {e}"}

def exportjson():
    cursor.execute('SELECT id, item_name, price, quantity FROM inventory')
    rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append(dict(zip([description[0] for description in cursor.description], row)))

    # Write the data to a JSON file
    with open('inventory.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


def shutdown_event():
    conn.close()

###INVENTORY TABLE OPERTATIONS END###


###TRANSACTION TABLE OPERATIONS###
def order(item_id: int, qty: int):
    #orders a quantity of the item and creates an entry in the order history table

    try:
        # Find the item in the inventory and get its current quantity
        cursor.execute('SELECT item_name, quantity, price FROM inventory WHERE id = ?', (item_id,))
        item_info = cursor.fetchone()

        if item_info is None:
            return {"message": "Item not found"}

        item_name, current_quantity, item_price = item_info

        # Calculate the new quantity after adding qty
        new_quantity = current_quantity + qty
        cost = item_price * qty

        # Update the quantity in the inventory table
        add_quantity(item_name, qty)

        #cursor.execute('UPDATE inventory SET quantity = ? WHERE id = ?', (new_quantity, item_id))
        conn.commit()

        # Insert a new row into the orderhistory table
        cursor.execute('INSERT INTO orderhistory (item_id, cost, quantity) VALUES (?, ?, ?)',
                       (item_id, cost, qty))  # You need to specify the actual price and price_per_item values
        conn.commit()

        return {"message": f"Ordered {qty} {item_name}(s)"}

    except sqlite3.Error as e:
        return {"message": f"Error: {e}"}

def void_order(transaction_id: int):
    #Void an order by the transaction id

    try:
        # Check if the transaction exists in the orderhistory table
        cursor.execute('SELECT * FROM orderhistory WHERE transaction_id = ?', (transaction_id,))
        existing_transaction = cursor.fetchone()

        if existing_transaction is None:
            return {"message": "Transaction not found"}

        # Delete the transaction from the orderhistory table
        cursor.execute('DELETE FROM orderhistory WHERE transaction_id = ?', (transaction_id,))
        conn.commit()

        return {"message": f"Transaction {transaction_id} voided"}

    except sqlite3.Error as e:
        return {"message": f"Error: {e}"}

def display_transaction_table():
    #display the transaction table

    try:
        # Execute a SELECT query to retrieve all entries from the orderhistory table
        cursor.execute('SELECT * FROM orderhistory')
        transactions = cursor.fetchall()

        if not transactions:
            return {"message": "No transactions found"}

        # Create a PrettyTable to display the transactions
        table = PrettyTable()
        table.field_names = ["Transaction ID", "Item ID", "Transaction Date", "Price", "Quantity"]

        for transaction in transactions:
            table.add_row(transaction)

        return {"message": "Transactions:", "table": table.get_string()}

    except sqlite3.Error as e:
        return {"message": f"Error: {e}"}
###END OF TRANSACION OPERATIONS###

###TESTING

#item = Item.create_basic(item_name = "candy", price=0.99) 
#item2 = Item.create_basic(item_name = "chips", price = 1.99)
#
#create_item(item2)
#
#
#print(get_items())
#
#order(3, 30)
#
## Example usage:
#inventory = display_inventory_table()
#if "table" in inventory:
#    print(inventory["message"])
#    print(inventory["table"])
#else:
#    print(inventory["message"])
#
#result = display_transaction_table()
#if "table" in result:
#    print(result["message"])
#    print(result["table"])
#else:
#    print(result["message"])
#
#shutdown_event()
