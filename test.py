from model import Item
import milkisdatabase as mkb
from fastapi import FastAPI

running = True

while running:
    print("\nWelcome to the Manager Portal. Please select an option:")
    print("1. View Inventory")
    print("2. Order Inventory")
    print("3. Export JSON")
    print("4. View Transactions")
    print("5. Add Item")
    print("4. Remove Item")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == '1':
        inventory = mkb.display_inventory_table()
        if "table" in inventory:
            print(inventory["message"])
            print(inventory["table"])
        else:
            print(inventory["message"])


    elif choice == '2':
        # Option: Order Inventory
        item_id = int(input("Enter the Item ID you want to order: "))
        quantity = int(input("Enter the quantity to order: "))
        try:
            print(mkb.order(item_id, quantity))
        except:
            print("[error] Item not found")

    elif choice == '3':
        mkb.exportjson()


    elif choice == '4':
        result = mkb.display_transaction_table()
        if "table" in result:
            print(result["message"])
            print(result["table"])
        else:
            print(result["message"])

    elif choice == '5':
        item_name = input("Please enter the name of the item you would like to add: ")
        item_price= float(input("Please enter the cost of this item(float): "))
        try:
            item = Item.create_basic(item_name = item_name, price=item_price)
            mkb.create_item(item)
        except:
            print("Error, item may already be in database")

    elif choice == '6':
        item_id = int(input("Please enter the ID of the item you would like to remove: "))
        try:
          mkb.delete_itemID(item_id)  
        except:
            print("[error] Item not found")

    elif choice == '7':
        # Option: Exit
        print("Exiting Manager Portal. Goodbye!")
        running = False

    else:
        print("Invalid choice. Please enter a number between 1 and 5.")


#need to create Item pydantic model first
#item = Item.create_basic(item_name = "candy", price=0.99) 
#item2 = Item.create_basic(item_name = "chips", price = 1.99)
#item3 = Item.create_basic(item_name = "turtle", price = 10.99)
#
#
##mkb.create_item(item)
#mkb.create_item(item3)
#
#print(mkb.order(1, 30))
#
#mkb.exportjson()
#
##example usage
#
