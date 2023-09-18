# MilkisVendingSystem
Full-System Development project for a vending machine business. Uses fastAPI and sqlalchemy for the backend(sqlite for teaching)

UML Diagram:
![alt text](https://github.com/galbii/MilkisVendingSystem/blob/dev/src/MilkisSystemPrototype.png)

#Installation
1. Clone the repository
```shell
$ git clone https://github.com/galbii/MilkisVendingSystem/
```
2. CD into the directory
```shell
$ cd MilkisVendingMachine
```
3. Activate the environment
```shell
$ source milkisenv/bin/activate
```
4. Install dependencies
```shell
$ pip install -r requirements.txt
```
5. Enjoy!

#SCHEMA AND DATABASE
We are using the Milkis.db as an sqlite database with the following tables:
Inventory:
+----+--------------+-------+-----------------+----------+
| ID | Product Name | Price | Product Company | Quantity |
+----+--------------+-------+-----------------+----------+
Transactions:
+----------------+------------+---------------------+-------+----------+
| Transaction ID | Product ID |   Transaction Date  | Price | Quantity |
+----------------+------------+---------------------+-------+----------+
