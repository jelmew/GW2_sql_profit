import sqlite3
from gw2_wrapper import *
db_name=''

def set_db_name(input_db_name):
    global db_name
    db_name=input_db_name
def create_tables():
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    c.execute('CREATE TABLE items (gw2_id INT PRIMARY KEY, gw2_name Varchar)')
    c.execute('CREATE TABLE tp_sold (id INT, gw2_id INT, price FLOAT, quantity INT, date_listed DATETIME )')
    c.execute('CREATE TABLE tp_selling (id INT, gw2_id INT, price FLOAT, quantity INT, date_listed DATETIME )')
    c.execute('CREATE TABLE tp_bought (id INT, gw2_id INT, price FLOAT, quantity INT, date_listed DATETIME )')
    c.execute('CREATE TABLE tp_buying (id INT, gw2_id INT, price FLOAT, quantity INT, date_listed DATETIME )')
   # c.execute('CREATE TABLE tp_listing (gw2_id INT,sell FLOAT, selldate DATE)')
    conn.commit()
    conn.close()


def insert_tp_items(sold_items_query,tp_database):
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    c.execute('SELECT id, gw2_id from {} ORDER BY id DESC'.format(tp_database))
    limit=int(0)
    gw2_id=0
    first_entry=c.fetchone()
    if first_entry!=None:
        limit=int(first_entry[0])
        gw2_id=int(first_entry[1])
    #if limit !=0: print get_name_from_id(gw2_id)
    #print limit
    #print sold_items_query
    for item in sold_items_query:
        if item['id']<= limit: continue
        t=(item['id'],item['item_id'],item['price'],item['quantity'],item['created'])
        #print t
        c.execute('INSERT INTO {} (id, gw2_id,price, quantity,date_listed) VALUES(?,?,?,?,?)'.format(tp_database),t)
    conn.commit()
    conn.close()

def update_tp_sold():
    t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/history/sells")
    insert_tp_items(t,'tp_sold')

def update_tp_selling():
    t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/current/sells")
    insert_tp_items(t,'tp_selling')
    
def update_tp_bought():
    t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/history/buys")
    insert_tp_items(t,'tp_bought')
    
def update_tp_buying():
    t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/current/buys")
    insert_tp_items(t,'tp_buying')
    
def insert_id_names():

    
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    c.execute('SELECT distinct gw2_id FROM (select gw2_id from tp_sold union all select gw2_id from tp_selling union all select gw2_id from tp_buying union all select gw2_id from tp_bought);')
    id_list= c.fetchall()
    for gw2_id_tup in id_list:
        gw2_id=gw2_id_tup[0]
        gw2_input_tup=(gw2_id,get_name_from_id(gw2_id))
        print gw2_input_tup
        c.execute('INSERT OR IGNORE INTO items VALUES(?, ?);',gw2_input_tup)
        #c.execute('insert')
        #c.execute('if NOT exists (select gw2_id from items where gw2_id =  ?) INSERT into items values (?)',gw2_insert_tup)
        
    conn.commit()
    conn.close()