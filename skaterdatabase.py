import sqlite3 as lite
# This class will be used for handling the contact with the
# database that will store the skaters.

columns = ['index', 'lastname', 'firstname', 'city', 'state', 'country', 'latitude', 'longitude']
db_file = 'skaters.db'

create_table = """DROP TABLE IF EXISTS Skaters;
        CREATE TABLE Skaters(Id INTEGER PRIMARY KEY, lastname TEXT, firstname TEXT, city TEXT, state TEXT, country TEXT,
         latitude REAL, longitude REAL);"""

con = lite.connect(db_file)

with con:
    cur = con.cursor()
    cur.executescript(create_table)

con.commit()

# TODO: Create an ORM
# Queries

# Get all skaters that played on x year
# Get all skaters that played on x year from x team