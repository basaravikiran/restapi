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


def create_duplicate_item(address, port, data):
    url = 'http://{}:{}/items/'.format(address, port)
    payload = json.dumps(eval(data))
    resp1 = requests.post(url, payload)
    resp2 = requests.post(url, payload)
    logger.info(resp1.text, True, True)
    logger.info(resp2.text, True, True)
    _assert_equal(resp1.status_code, 201)
    _assert_equal(resp2.status_code, 400)

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

def delete_non_default_items(address, port):
    url = 'http://{}:{}/items/'.format(address, port)
    resp = requests.get(url)
    _assert_equal(resp.status_code, 200)
    data=json.loads(resp.text)
    default_names=["item_0","item_1","item_2", "item_3","item_4"]
    for item in data:
        name=item['name']
        if name not in default_names :
            delete_item(address,port,name)


def main():
    url='127.0.0.1'
    port=5000
    data=str({'name': 'akku1', 'serial': '5002'})
    delete_non_default_items(url,port)

if __name__=='__main__':main()