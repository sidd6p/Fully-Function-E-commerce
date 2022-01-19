import sqlite3

def dbquery(query, data):
    dbAddress = r'C:\Users\siddpc\OneDrive\Desktop\Projects\offline-e-commerce\databases\product.db'
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    connection.close()