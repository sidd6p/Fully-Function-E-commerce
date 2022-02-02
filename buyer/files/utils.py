import sqlite3
from files.models import Buyer
from files import db
from files.config import DB_ADDRESS

def dbquery(query, data):
    dbAddress = DB_ADDRESS
    connection = sqlite3.connect(dbAddress)
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    connection.close()

def add_buyer(form_data):
    newBuyer = Buyer(fname = form_data.buyerFirstName.data,\
                    lname = form_data.buyerLastName.data,\
                    email = form_data.email.data,\
                    password = form_data.pswd.data,\
                    address = form_data.address.data,\
                    city = form_data.city.data,\
                    state = form_data.state.data,\
                    pin = form_data.pin.data)
    db.session.add(newBuyer)
    db.session.commit()