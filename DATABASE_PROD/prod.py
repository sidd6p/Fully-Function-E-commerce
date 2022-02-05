import sqlite3

connection = sqlite3.connect('product.db')
cursor = connection.cursor()

# query = "CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, productName VARCHAR(100) NOT NULL, productType VARCHAR(100) NOT NULL, productPhoto VARCHAR(200) NOT NULL, productDesc VARCHAR(500) NOT NULL, productPrice INTEGER NOT NULL, sellerAddress VARCHAR(100) NOT NULL, sellerName VARCHAR(100) NOT NULL, sellerEmail VARCHAR(100) NOT NULL, sellerID INTEGER NOT NULL )"

query = "ALTER TABLE products RENAME COLUMN sellerName TO shopName"
cursor.execute(query)
connection.commit()
connection.close()

