import requests

def get_jsonparsed_data(url):
    #Receive contect as url returned as object"
    response=requests.get(url)
    return response.json()

def get_jsonpared_data_auth(url):
    key="D37ED73D-3BA9-9D4B-B0CB-CB5F91E03E12B99BA2F6-843B-494E-B65A-03B35A5556F6"
    url=url+"?access_token="+key
    response=requests.get(url)
    return response.json()


def get_name_from_id(gw2_id):
    url='https://api.guildwars2.com/v2/items/'+str(gw2_id)
    json_object=get_jsonparsed_data(url)
    name=json_object["name"]
    return name

def get_sold_items():
    t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/history/sells")
    return t

def get_selling_items():
    t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/current/sells")
    return t

def get_bought_items():
    t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/history/buys")
    return t

def get_buying_items():
   t=get_jsonpared_data_auth("https://api.guildwars2.com/v2/commerce/transactions/current/buys")
   return t


