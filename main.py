import os.path


from lib.gw2_object import *
from lib.database import *
from lib.gw2_wrapper import *

api_key=''
if __name__ == '__main__':
    fname='test.db'
    set_db_name(fname)
    if not os.path.isfile(fname):create_tables()

    set_api_key(api_key)
    update_tp_sold()
    update_tp_selling()
    update_tp_buying()
    update_tp_bought()
    insert_id_names()
    update_current_price()
    sellable_for_profit()
    #get_list_of_unsold_items()
    #print get_bought_items()
    #name =get_name_from_id(28445)
    #print name
    #test=gw2_item_tp(28446)
    #print test.name
    #print test.sell_price
    #t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/history/sells")
    #insert_tp_items('test.db',t,'tp_sold')
    #print t
    