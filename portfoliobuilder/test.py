import sqlite3

from portfoliobuilder.builder import Basket

# Establish connection with database file
conn = sqlite3.connect('portfoliobuilder/portfoliobuilder.db')

# Create a Cursor object so that you can execute commands
cursor = conn.cursor()

# # Save changes to database
# conn.commit()

# # Close connection
# conn.close()

# # Create table
# cursor.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')

# # Insert 'RHAT' into the 'stocks' table
# t = ('RHAT',)
# cursor.execute('INSERT INTO stocks VALUES ?', t)

# # Insert multiple rows into the 'stocks' table
# t = [('RHAT',), ('AAPL',), ('GOOG',)]
# cursor.execute('INSERT INTO stocks VALUES (?,?,?)')

# # Print all rows in the 'stocks' table
# for row in cursor.execute('SELECT * FROM stocks'):
#     print(row)

cursor.execute('UPDATE baskets SET active=? WHERE name=?', (0,'Basket0'))
# cursor.execute('UPDATE baskets SET weighting_method=? WHERE name=?', ('value_quality','Basket1'))


conn.commit()
conn.close()