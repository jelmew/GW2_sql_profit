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
    c.execute('CREATE TABLE tp_sold (id INT PRIMARY KEY, gw2_id INT, price FLOAT, quantity INT, date_listed DATETIME )')
    c.execute('CREATE TABLE tp_selling (id INT PRIMARY KEY, gw2_id INT, price FLOAT, quantity INT, date_listed DATETIME )')
    c.execute('CREATE TABLE tp_bought (id INT PRIMARY KEY, gw2_id INT, price FLOAT, quantity INT, date_listed DATETIME )')
    c.execute('CREATE TABLE tp_buying (id INT PRIMARY KEY, gw2_id INT, price FLOAT, quantity INT, date_listed DATETIME )')
    c.execute('CREATE TABLE tp_prices (gw2_id INT PRIMARY KEY, price FLOAT);')
   # c.execute('CREATE TABLE tp_listing (gw2_id INT,sell FLOAT, selldate DATE)')
    conn.commit()
    conn.close()

def return_list_of_transaction_items():
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    #c.execute('SELECT distinct gw2_id')
    c.execute('SELECT distinct gw2_id FROM (select gw2_id from tp_sold union all select gw2_id from tp_selling union all select gw2_id from tp_buying union all select gw2_id from tp_bought);')
    id_list= c.fetchall()
    #print id_list
    conn.commit()
    conn.close()
    return id_list

def insert_tp_items(sold_items_query,tp_database):
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    for item in sold_items_query:
        t=(item['id'],item['item_id'],item['price'],item['quantity'],item['created'])
        c.execute('INSERT OR IGNORE INTO {} (id, gw2_id,price,quantity,date_listed) VALUES(?,?,?,?,?)'.format(tp_database),t)
    conn.commit()
    conn.close()

def insert_tp_items_old(sold_items_query,tp_database):
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    c.execute('SELECT id, gw2_id from {} ORDER BY id DESC'.format(tp_database))
    limit=int(0)
    gw2_id=0
    first_entry=c.fetchone()
    if first_entry!=None:
        limit=int(first_entry[0])
        gw2_id=int(first_entry[1])
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
    id_list=return_list_of_transaction_items()
    for gw2_id_tup in id_list:
        gw2_id=gw2_id_tup[0]
        gw2_input_tup=(gw2_id,get_name_from_id(gw2_id))
        #print gw2_input_tup
        #print gw2_input_tup
        c.execute('INSERT OR IGNORE INTO items VALUES(?, ?);',gw2_input_tup)
        conn.commit()
        #c.execute('insert')
        #c.execute('if NOT exists (select gw2_id from items where gw2_id =  ?) INSERT into items values (?)',gw2_insert_tup)
        
    conn.commit()
    conn.close()

def update_current_price():
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    c.execute('SELECT DISTINCT gw2_id FROM tp_bought')
    list_of_all_items=c.fetchall()
    for item in list_of_all_items:
        gw2_id=item[0]
        t=get_price_item(gw2_id)
        insert_tuple=(gw2_id,gw2_id,t['sells']['unit_price'])
        c.execute('INSERT OR REPLACE INTO tp_prices (gw2_id,price) VALUES (COALESCE((SELECT gw2_id FROM tp_prices WHERE gw2_id=?),?) ,?);',insert_tuple)
    conn.commit()
    conn.close()

def get_list_of_unsold_items():
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    #c.execute('SELECT gw2_id, price, quantity FROM tp_bought')
    #list_of_gw2_id=c.fetchall()
    #print list_of_gw2_id
    c.execute('SELECT b.gw2_id, b.price, sum(b.quantity) FROM tp_bought b INNER JOIN tp_bought b2 on b.gw2_id=b2.gw2_id and b.price=b2.price GROUP BY b.gw2_id')
    list_of_gw2_id_bought=list(c.fetchall())
    list_of_gw2_id_bought=[list(elem) for elem in list_of_gw2_id_bought]
    c.execute('SELECT b.gw2_id, b.price, sum(b.quantity) FROM tp_sold b INNER JOIN tp_sold b2 on b.gw2_id=b2.gw2_id and b.price=b2.price GROUP BY b.gw2_id')
    list_of_gw2_id_sold=list(c.fetchall())
    list_of_gw2_id_sold=[list(elem) for elem in list_of_gw2_id_sold]
    c.execute('SELECT b.gw2_id, b.price, sum(b.quantity) FROM tp_selling b INNER JOIN tp_selling b2 on b.gw2_id=b2.gw2_id and b.price=b2.price GROUP BY b.gw2_id')
    list_of_gw2_id_selling=list(c.fetchall())
    list_of_gw2_id_selling=[list(elem) for elem in list_of_gw2_id_selling]
    #gw2_id_only_sold_list=[x[0] for x in list_of_gw2_id_sold[0]]
    print list_of_gw2_id_selling
    sold_item_match=[]
    for index, bought in enumerate(list_of_gw2_id_bought):
        print bought
        if bought[0] in [x[0] for x in list_of_gw2_id_sold]:
            sold_item_match=[x for x in  list_of_gw2_id_sold if x[0]==bought[0]]
            for sold_item in sold_item_match:
                bought[2]=bought[2]-sold_item[2]
        print bought
        
 
 
def sellable_for_profit():
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    #c.execute('SELECT  i.gw2_name,b.gw2_id, SUM(b.quantity) AS sum_quantity, b.price, p.price FROM tp_bought b INNER JOIN items i ON b.gw2_id=i.gw2_id INNER JOIN tp_prices p ON p.gw2_id=b.gw2_id   GROUP BY b.price, b.gw2_id')
    #test=c.fetchall()
    #print test
    c.execute('SELECT  i.gw2_name,b.gw2_id, SUM(b.quantity) AS sum_quantity, b.price, p.price FROM tp_bought b INNER JOIN items i ON b.gw2_id=i.gw2_id INNER JOIN tp_prices p ON p.gw2_id=b.gw2_id  WHERE p.price*0.85> b.price GROUP BY b.price, b.gw2_id')

    list_of_items=c.fetchall()
    print list_of_items
    for item in list_of_items:
        profit_percentage=(float(item[4]/item[3])-1)*100
        print "Item {} can be sold with {}%  profit".format(item[0],profit_percentage)
