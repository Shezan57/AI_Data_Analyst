import sqlite3

# Step 1: Create a dummy database
conn = sqlite3.connect("amazon.db")
cursor = conn.cursor()

# Step 2: Create a sample table

# Table: Customers, orders, products, order_items

cursor.execute("""
               CREATE TABLE IF NOT EXISTS customers(
                   customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   email TEXT,
                   address TEXT,
                   phone TEXT,
                   joined_date TEXT)""")

cursor.execute("""
               CREATE TABLE IF NOT EXISTS orders(
                   order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_id INTEGER,
                   order_date TEXT,
                   status TEXT,
                   total_amount REAL,
                   FOREIGN KEY (customer_id) REFERENCES customers (customer_id))""")

cursor.execute("""
               CREATE TABLE IF NOT EXISTS products(
                   product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   description TEXT,
                   price REAL,
                   stock_quantity INTEGER)""")

cursor.execute("""
               CREATE TABLE IF NOT EXISTS order_items(
                   order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   order_id INTEGER,
                   product_id INTEGER,
                   quantity INTEGER,
                   price REAL,
                   FOREIGN KEY (order_id) REFERENCES orders (order_id),
                   FOREIGN KEY (product_id) REFERENCES products (product_id))""")

# Step 3 Enter dummy data into the tables

customers = [
    ("John Doe", "john@example.com", "123 Elm St", "555-1234", "2023-01-01"),
    ("Jane Smith", "jane@example.com", "456 Oak St", "555-5678", "2023-02-01"),
    ("Alice Johnson", "alice@example.com", "789 Pine St", "555-8765", "2023-03-01"),
    ("Bob Brown", "bob@example.com", "321 Maple St", "555-4321", "2023-04-01"),
    ("Charlie Davis", "charlie@example.com", "654 Cedar St", "555-9876", "2023-05-01"),
    ("David Wilson", "david@example.com", "987 Birch St", "555-2468", "2023-06-01"),
    ("Eva Martinez", "eva@example.com", "159 Spruce St", "555-1357", "2023-07-01")
]


cursor.executemany("""
                INSERT INTO customers (name, email, address, phone, joined_date)
                VALUES (?, ?, ?, ?, ?)""", customers)
orders = [
    (1, "2023-04-01", "Shipped", 150.00),
    (2, "2023-04-02", "Processing", 200.00),
    (3, "2023-04-03", "Delivered", 300.00),
    (4, "2023-04-04", "Cancelled", 400.00),
    (5, "2023-04-05", "Shipped", 500.00),
    (6, "2023-04-06", "Processing", 600.00),
    (7, "2023-04-07", "Delivered", 700.00)
]


cursor.executemany("""
                INSERT INTO orders (customer_id, order_date, status, total_amount)
                VALUES (?, ?, ?, ?)""", orders)
products = [
    ("Laptop", "A high-performance laptop", 1000.00, 10),
    ("Smartphone", "A latest model smartphone", 800.00, 20),
    ("Tablet", "A lightweight tablet", 600.00, 15),
    ("Headphones", "Noise-cancelling headphones", 200.00, 30),
    ("Smartwatch", "A smartwatch with various features", 300.00, 25),
    ("Camera", "A digital camera", 500.00, 12),
    ("Printer", "A wireless printer", 150.00, 18),
    ("Monitor", "A 24-inch monitor", 250.00, 14),
    ("Keyboard", "A mechanical keyboard", 100.00, 40),
    ("Mouse", "A wireless mouse", 50.00, 50),
    ("Webcam", "A high-definition webcam", 75.00, 20)
]

cursor.executemany("""
                INSERT INTO products (name, description, price, stock_quantity)
                VALUES (?, ?, ?, ?)""", products)
order_items = [
    (1, 1, 1, 1000.00),
    (2, 1, 2, 800.00),
    (3, 2, 3, 600.00),
    (4, 2, 4, 200.00),
    (5, 3, 5, 300.00),
    (6, 3, 6, 500.00),
    (7, 4, 7, 150.00),
    (8, 4, 8, 250.00),
    (9, 5, 9, 100.00),
    (10, 5, 10, 50.00),
    (11, 6, 11, 75.00)
]


cursor.executemany("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)""", order_items)
# Commit the changes and close the connection
conn.commit()
conn.close()
print("Database and tables created with dummy data.")
