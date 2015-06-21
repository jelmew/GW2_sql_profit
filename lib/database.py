import sqlite3

def create_tables(db_name):
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    c.execute('CREATE TABLE items (gw2_id INT, gw2_name Varchar, quantity INT)')

    c.execute('CREATE TABLE tp_listing (gw2_id INT,sell FLOAT)')
    conn.commit()
    conn.close()
