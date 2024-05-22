import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime, timedelta

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='rajat',
            password='rajat',
            database='flow_shipping'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_merchants(connection, num_merchants=5):
    faker = Faker()
    cursor = connection.cursor()
    for _ in range(num_merchants):
        name = faker.company()
        cursor.execute("INSERT INTO merchants (name) VALUES (%s)", (name,))
    connection.commit()

def create_carriers(connection):
    cursor = connection.cursor()
    carriers = [
        ('Carrier A', 250, 2, 5.00),
        ('Carrier B', 200, 4, 9.00),
        ('Carrier C', 150, 8, 15.00),
        ('Carrier D', 100, 16, 25.00),
        ('Carrier E', 50, 32, 40.00)
    ]
    for carrier in carriers:
        cursor.execute("INSERT INTO carriers (name, max_orders, max_pieces, cost_per_order) VALUES (%s, %s, %s, %s)", carrier)
    connection.commit()

def create_merchandise(connection, min_items=100, max_items=500):
    faker = Faker()
    cursor = connection.cursor()
    cursor.execute("SELECT merchant_id FROM merchants")
    merchants = cursor.fetchall()
    for merchant in merchants:
        merchant_id = merchant[0]
        for _ in range(random.randint(min_items, max_items)):
            name = faker.word()
            cursor.execute("INSERT INTO merchandise (merchant_id, name) VALUES (%s, %s)", (merchant_id, name))
    connection.commit()

def create_orders(connection, min_orders=400, max_orders=650):
    faker = Faker()
    cursor = connection.cursor()
    cursor.execute("SELECT merchant_id FROM merchants")
    merchants = cursor.fetchall()
    cursor.execute("SELECT carrier_id, max_pieces, max_orders FROM carriers")
    carriers = cursor.fetchall()

    for _ in range(random.randint(min_orders, max_orders)):
        merchant_id = random.choice(merchants)[0]
        pieces = random.randint(1, 50)

        # Find a suitable carrier
        for carrier in carriers:
            carrier_id, max_pieces, max_orders = carrier
            if pieces <= max_pieces:
                cursor.execute("SELECT COUNT(*) FROM orders WHERE carrier_id = %s AND DATE(shipped_date) = CURDATE()", (carrier_id,))
                orders_today = cursor.fetchone()[0]
                if orders_today < max_orders:
                    shipped_date = datetime.now().date()
                    cursor.execute("INSERT INTO orders (merchant_id, pieces, shipped, carrier_id, shipped_date) VALUES (%s, %s, %s, %s, %s)", 
                                   (merchant_id, pieces, True, carrier_id, shipped_date))
                    connection.commit()
                    break

if __name__ == "__main__":
    connection = create_connection()
    
    # Populate the tables with random data
    create_merchants(connection, num_merchants=5)
    create_carriers(connection)
    create_merchandise(connection, min_items=100, max_items=500)
    create_orders(connection, min_orders=400, max_orders=650)
    
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
