import sqlite3

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return connection

def create_table(connection,create_table_sql):
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        connection.commit()
    except sqlite3.Error as e:
        print(e)

sql_create_table_products = '''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_title VARCHAR(200) NOT NULL,
    price FLOAT(10, 2) NOT NULL DEFAULT 0.0,
    quantity INTEGER NOT NULL DEFAULT 0
)'''

def insert_products(connection,products):
    sql = '''INSERT INTO products(product_title,price,quantity)
    VALUES (?, ?, ?)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql,products)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def quantity_on_id(connection,product_id,new_quantity):
    sql = '''UPDATE products
            SET quantity = ?
            WHERE id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql,(new_quantity,product_id))
        connection.commit()
    except sqlite3.Error as e:
        print(e)

def price_on_id(connection,product_id,new_price):
    sql = '''UPDATE products
             SET price = ?
             WHERE id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (new_price, product_id))
        connection.commit()
    except sqlite3.Error as e:
        print(e)

def delete_product(connection,product_id):
    sql = '''DELETE FROM products WHERE id = ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (product_id,))
        connection.commit()
    except sqlite3.Error as e:
        print(e)

def select_all_products(connection):
    sql = '''SELECT * FROM products'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)

def select_products_price_quantity(connection,price_limit,quantity_limit):
    sql = '''SELECT * FROM products WHERE price < ? AND quantity > ?'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql,(price_limit,quantity_limit))
        rows = cursor.fetchall()
        if rows:
            print(f"Товары с ценой меньше {price_limit} и количеством больше {quantity_limit}:")
            for row in rows:
                print(row)
        else:
            print("Продукты с заданными условиями не найдены.")
    except sqlite3.Error as e:
        print(e)

def like_product(connection,search_term):
    sql = '''SELECT * FROM products WHERE LOWER(product_title) LIKE LOWER(?) '''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, ('%' + search_term + '%',))
        rows = cursor.fetchall()

        if rows:
            print(f"Товары, содержащие '{search_term}':")
            for row in rows:
                print(row)
        else:
            print(f"Товары, содержащие '{search_term}', не найдены.")
    except sqlite3.Error as e:
        print(e)


my_conn = create_connection('hw.db')
if my_conn is not None:
    print('Successfuly connected to datebase')
    create_table(my_conn,sql_create_table_products)

insert_products(my_conn, ("Порошок", 100.0, 90))
insert_products(my_conn, ("Мыло", 200.0, 50))
insert_products(my_conn, ("Дезодорант спрей", 50.0, 100))
insert_products(my_conn, ("Средство для посуды", 90.0, 100))
insert_products(my_conn, ("Мыло хозяйственное", 45.0, 100))
insert_products(my_conn, ("Шампунь", 100.0, 30))
insert_products(my_conn, ("Гель для стирки", 150.0, 200))
insert_products(my_conn, ("Моющее средство", 50.0, 150))
insert_products(my_conn, ("Гель", 100.0, 90))
insert_products(my_conn, ("Кондиционер", 200.0, 50))
insert_products(my_conn, ("Дезодорант", 120.0, 200))
insert_products(my_conn, ("Средство для ванны", 90.0, 100))
insert_products(my_conn, ("Мыло жидкое", 45.0, 100))
insert_products(my_conn, ("Шампунь для густых волос", 100.0, 30))
insert_products(my_conn, ("Гель для душа", 105.0, 110))

quantity_on_id(my_conn,46, 200)
price_on_id(my_conn,48,150.0)
delete_product(my_conn, 57)
select_products_price_quantity(my_conn, 100, 50)
like_product(my_conn, "мыло")

select_all_products(my_conn)

my_conn.close()