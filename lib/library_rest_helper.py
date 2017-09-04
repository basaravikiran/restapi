import json
import requests
from robot.api import logger

def _assert_equal(a, b, message=None):
    if message is None:
        message = "Failed equal: {} == {}".format(a, b)
    assert a == b, message

def verify_server_is_running(address, port):
    url = 'http://{}:{}'.format(address, port)
    resp = requests.get(url)
    _assert_equal(resp.status_code, 200)
    _assert_equal(json.loads(resp.text), {'server': 'ok'})

def create_item(address, port, data):
    url = 'http://{}:{}/items/'.format(address, port)
    payload=json.dumps(eval(data))
    resp = requests.post(url,payload)
    logger.info(resp.text,True,True)
    _assert_equal(resp.status_code, 201)
    logger.info('Server Responce:' + resp.text, True, True)


def create_duplicate_item(address, port, data):
    url = 'http://{}:{}/items/'.format(address, port)
    payload = json.dumps(eval(data))
    resp1 = requests.post(url, payload)
    if resp1.status_code == 201:
        resp2 = requests.post(url, payload)
        _assert_equal(resp2.status_code, 400)
    else:
        _assert_equal(resp1.status_code, 400)


def verify_item_name_in_list(address, port, name):
    url = 'http://{}:{}/items'.format(address, port)
    resp = requests.get(url)
    _assert_equal(resp.status_code, 200)

    item_found = False
    content = json.loads(resp.text)
    for item in content:
        if item.get('name') == name:
            item_found = True
            break
    _assert_equal(item_found, True, "Item not found: {}".format(name))

def verify_item_name_not_in_list(address, port, name):
    url = 'http://{}:{}/items'.format(address, port)
    resp = requests.get(url)
    _assert_equal(resp.status_code, 200)

    item_found = False
    content = json.loads(resp.text)
    for item in content:
        if item.get('name') == name:
            item_found = True
            break
    _assert_equal(item_found, False, "Item found: {}".format(name))

def delete_item(address, port, name):
    url = 'http://{}:{}/items/{}'.format(address, port,name)
    resp = requests.delete(url)
    _assert_equal(resp.status_code,204)

def reset_default_items(address, port):
    url = 'http://{}:{}/items/'.format(address, port)
    resp = requests.get(url)
    _assert_equal(resp.status_code, 200)
    data=json.loads(resp.text)
    logger.info(data, True, True)
    default_names=["item_0","item_1","item_2", "item_3","item_4"]
    names=[]
    for item in data:
        name=item['name']
        if name in default_names :
            names.append(name)
        else:
            delete_item(address,port,name)

    diff_names=list(set(default_names)-set(names))
    for value in diff_names:
        data={}
        data['name']=value
        create_item(address,port,str(data))
    logger.info('diff_names:'+str(diff_names), True, True)


def main():
    url='127.0.0.1'
    port=5000
    data=str({'name': 'akku1', 'serial': '5002'})
    delete_non_default_items(url,port)

if __name__=='__main__':main()