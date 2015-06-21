from gw2_wrapper import *
import requests

class gw2_item(object):

    def __init__(self,gw2_id):
        self.gw2_id=gw2_id
        self.get_name_from_id()
        
    def get_name_from_id(self):
        url="https://api.guildwars2.com/v2/items/"
        url_id=url+str(self.gw2_id)
        json_struct=get_jsonparsed_data(url_id)
        self.name=str(json_struct["name"])
        


class gw2_item_tp(gw2_item):
    def __init__(self,gw2_id):
        super(gw2_item_tp,self).__init__(gw2_id)
        self.sell_price=0
        self.buy_price=0
        self.get_tp_values()
        
        
    def get_tp_values(self):
        url="https://api.guildwars2.com/v2/commerce/listings/"+str(self.gw2_id)
        json_struct=get_jsonparsed_data(url)
        #buy_array=json_struct['buys']
        self.sell_price=json_struct['sells'][0]['unit_price']
        #print buy_array[0]['unit_price']
        

