import requests

def get_jsonparsed_data(url):
    #Receive contect as url returned as object"
    response=requests.get(url)
    return response.json()

def get_jsonpared_data_auth(url):
    key="D37ED73D-3BA9-9D4B-B0CB-CB5F91E03E12B99BA2F6-843B-494E-B65A-03B35A5556F6"
    url="https://api.guildwars2.com/v2/commerce/transactions/history/sells?access_token="+key
    response=requests.get(url)
    return response.json()


def get_name_from_id(gw2_id):
    url='https://api.guildwars2.com/v2/items/'+str(gw2_id)
    json_object=get_jsonparsed_data(url)
    #print json_object
    name=json_object["name"]
    return name


