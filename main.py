import os.path


from lib.gw2_object import *
from lib.database import *
from lib.gw2_wrapper import *

api_key="D37ED73D-3BA9-9D4B-B0CB-CB5F91E03E12B99BA2F6-843B-494E-B65A-03B35A5556F6"
if __name__ == '__main__':
    fname='test.db'
    set_db_name(fname)
    if not os.path.isfile(fname):create_tables()


    update_tp_sold()
    update_tp_selling()
    update_tp_buying()
    update_tp_bought()
    #print get_bought_items()
    #name =get_name_from_id(28445)
    #print name
    #test=gw2_item_tp(28446)
    #print test.name
    #print test.sell_price
    #t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/history/sells")
    #insert_tp_items('test.db',t,'tp_sold')
    #print t
    