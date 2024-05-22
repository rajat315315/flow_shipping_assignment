import mysql.connector
from mysql.connector import Error
from datetime import datetime

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

def get_available_carriers(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carriers")
    return cursor.fetchall()

def get_orders_to_ship(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE shipped = False")
    return cursor.fetchall()

def assign_carrier_to_order(connection, order_id, carrier_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO orders (order_id, carrier_id, status) VALUES (%s, %s, %s)", (order_id, carrier_id, 'assigned'))
    connection.commit()

def mark_order_as_shipped(connection, order_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE orders SET status = 'shipped' WHERE order_id = %s", (order_id,))
    connection.commit()

def get_orders_by_carrier(connection, carrier_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE carrier_id = %s", (carrier_id,))
    return cursor.fetchall()

def assign_most_economical_carrier(connection, order):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carriers ORDER BY cost_per_order ASC")
    carriers = cursor.fetchall()
    for carrier in carriers:
        cursor.execute("SELECT SUM(quantity) as total_items FROM Orders WHERE order_id = %s", (order['order_id'],))
        total_items = cursor.fetchone()['total_items']
        if total_items <= carrier['max_items']:
            cursor.execute("SELECT COUNT(*) as orders_today FROM Orders WHERE carrier_id = %s AND shipped_date = %s", (carrier['carrier_id'], datetime.now()))
            orders_today = cursor.fetchone()['orders_today']
            if orders_today < carrier['max_orders']:
                assign_carrier_to_order(connection, order['order_id'], carrier['carrier_id'])
                return

if __name__ == "__main__":
    connection = create_connection()

    # Example usage:
    orders = get_orders_to_ship(connection)
    for order in orders:
        assign_most_economical_carrier(connection, order)
    for order in orders:
        mark_order_as_shipped(connection, order['order_id'])
    carriers = get_available_carriers(connection)
    for carrier in carriers:
        assigned_orders = get_orders_by_carrier(connection, carrier['carrier_id'])
        print(f"Orders assigned to {carrier['name']}: {assigned_orders}")
