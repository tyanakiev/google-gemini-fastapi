import sqlite3
from datetime import datetime
import random

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('orders.db')
c = conn.cursor()

# Create the Orders table with important columns
c.execute('''CREATE TABLE IF NOT EXISTS Orders
             (HEADER_ID INTEGER PRIMARY KEY, ORG_ID INTEGER, ORDER_NUMBER INTEGER NOT NULL, ORDER_TYPE_ID INTEGER NOT NULL, ORDERED_DATE DATE, CUST_PO_NUMBER VARCHAR(50), SOLD_TO_ORG_ID INTEGER, SHIP_TO_ORG_ID INTEGER, CREATION_DATE DATE NOT NULL, CREATED_BY INTEGER NOT NULL, OPEN_FLAG VARCHAR(1) NOT NULL, ORDER_CATEGORY_CODE VARCHAR(30) NOT NULL)''')

# Create the OrderLines table with important columns and a foreign key constraint
c.execute('''CREATE TABLE IF NOT EXISTS OrderLines
             (HEADER_ID INTEGER NOT NULL, LINE_ID INTEGER NOT NULL, LINE_NUMBER INTEGER NOT NULL, STATUS_CODE VARCHAR(120) NOT NULL, ORDERED_QTY INTEGER NOT NULL, ORDERED_UOM VARCHAR(12) NOT NULL, INVENTORY_ITEM_ID INTEGER NOT NULL, INVENTORY_ORGANIZATION_ID INTEGER NOT NULL, OPEN_FLAG VARCHAR(4) NOT NULL, SHIPPED_QTY INTEGER, CREATION_DATE TIMESTAMP NOT NULL, CREATED_BY VARCHAR(256) NOT NULL, LAST_UPDATE_DATE TIMESTAMP NOT NULL, LAST_UPDATED_BY VARCHAR(256) NOT NULL, FOREIGN KEY(HEADER_ID) REFERENCES Orders(HEADER_ID))''')

# Function to generate random data for Orders
def generate_order_data():
    org_id = random.randint(1, 100)
    order_number = random.randint(1000, 9999)
    order_type_id = random.randint(1, 5)
    ordered_date = datetime(random.randint(2020, 2024), random.randint(1, 12), random.randint(1, 28)).date()
    cust_po_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
    sold_to_org_id = random.randint(1, 100)
    ship_to_org_id = random.randint(1, 100)
    creation_date = datetime.now().date()
    created_by = random.randint(1, 100)
    open_flag = 'Y'
    order_category_code = 'ORD'

    return (org_id, order_number, order_type_id, ordered_date, cust_po_number, sold_to_org_id, ship_to_org_id, creation_date, created_by, open_flag, order_category_code)

# Function to generate random data for OrderLines
def generate_orderline_data(header_id):
    line_id = random.randint(1, 1000)
    line_number = random.randint(1, 100)
    status_code = 'NEW'
    ordered_qty = random.randint(1, 100)
    ordered_uom = 'EA'
    inventory_item_id = random.randint(1, 1000)
    inventory_organization_id = random.randint(1, 10)
    open_flag = 'Y'
    shipped_qty = 0
    creation_date = datetime.now()
    created_by = 'SYSTEM'
    last_update_date = datetime.now()
    last_updated_by = 'SYSTEM'

    return (header_id, line_id, line_number, status_code, ordered_qty, ordered_uom, inventory_item_id, inventory_organization_id, open_flag, shipped_qty, creation_date, created_by, last_update_date, last_updated_by)

# Insert 10 orders with random data
for _ in range(10):
    order_data = generate_order_data()
    c.execute("INSERT INTO Orders VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", order_data)
    header_id = c.lastrowid

    # Insert 2-3 order lines for each order
    for _ in range(random.randint(2, 3)):
        orderline_data = generate_orderline_data(header_id)
        c.execute("INSERT INTO OrderLines VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", orderline_data)

conn.commit()
conn.close()