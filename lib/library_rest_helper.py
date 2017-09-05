import json
import requests
from robot.api import logger

def _assert_equal(a, b, message=None):
    if message is None:
        message = "Failed equal: {} == {}".format(a, b)
    assert a == b, message

def verify_server_is_running(address, port):
    logger.info('Verifying server is running... ', True, True)
    url = 'http://{}:{}'.format(address, port)
    resp = requests.get(url)
    logger.info('Response Content:' +str(resp.text) , True, True)
    logger.info('Status Code:' + str(resp.status_code), True, True)
    _assert_equal(resp.status_code, 200)
    _assert_equal(json.loads(resp.text), {'server': 'ok'})

def create_item(address, port, data):
    logger.info('Creating item... ', True, True)
    url = 'http://{}:{}/items/'.format(address, port)
    payload=json.dumps(eval(data))
    resp = requests.post(url,payload)
    logger.info('Response Content:' + str(resp.text), True, True)
    logger.info('Status Code:' + str(resp.status_code), True, True)
    return resp.status_code,resp.text

def access_item_details(address, port, name):
    logger.info('Accessing item {}'.format(name)+'... ', True, True)
    url = 'http://{}:{}/items/{}'.format(address, port,name)
    resp = requests.get(url)
    logger.info('Response Content:' + str(resp.text), True, True)
    logger.info('Status Code:' + str(resp.status_code), True, True)
    return resp.status_code,resp.text

def access_items_list(address, port):
    logger.info('Accessing items list ... ', True, True)
    url = 'http://{}:{}/items/'.format(address, port)
    resp = requests.get(url)
    logger.info('Response Content:' + str(resp.text), True, True)
    logger.info('Status Code:' + str(resp.status_code), True, True)
    return resp.status_code,resp.text

def create_duplicate_item(address, port, data):
    logger.info('Trying to create duplicate item... ', True, True)
    url = 'http://{}:{}/items/'.format(address, port)
    payload = json.dumps(eval(data))
    resp1 = requests.post(url, payload)
    if resp1.status_code == 201:
        resp2 = requests.post(url, payload)
        logger.info('Response Content:' + str(resp2.text), True, True)
        logger.info('Status Code:' + str(resp2.status_code), True, True)
        return  resp2.status_code,resp2.text
    else:
        logger.info('Response Content:' + str(resp1.text), True, True)
        logger.info('Status Code:' + str(resp1.status_code), True, True)
        return resp1.status_code, resp1.text


def verify_item_name_in_list(address, port, name):
    logger.info('Verifying item name in list... ', True, True)
    url = 'http://{}:{}/items'.format(address, port)
    resp = requests.get(url)
    logger.info('Response Content:' + str(resp.text), True, True)
    logger.info('Status Code:' + str(resp.status_code), True, True)
    _assert_equal(resp.status_code, 200)

    item_found = False
    content = json.loads(resp.text)
    for item in content:
        if item.get('name') == name:
            item_found = True
            break
    _assert_equal(item_found, True, "Item not found: {}".format(name))

def verify_item_name_not_in_list(address, port, name):
    logger.info('Verifying item name  {} not in list... '.format(name), True, True)
    url = 'http://{}:{}/items'.format(address, port)
    resp = requests.get(url)
    logger.info('Response Content:' + str(resp.text), True, True)
    logger.info('Status Code:' + str(resp.status_code), True, True)
    _assert_equal(resp.status_code, 200)

    item_found = False
    content = json.loads(resp.text)
    for item in content:
        if item.get('name') == name:
            item_found = True
            break
    _assert_equal(item_found, False, "Item found: {}".format(name))

def delete_item(address, port, name):
    logger.info('Deleting the item  '+str(name)+'...', True, True)
    url = 'http://{}:{}/items/{}'.format(address, port,name)
    resp = requests.delete(url)
    logger.info('Response Content:' + str(resp.text), True, True)
    logger.info('Status Code:' + str(resp.status_code), True, True)
    status_code=resp.status_code
    content=resp.text
    url = 'http://{}:{}/items/'.format(address, port)
    resp = requests.get(url)
    logger.info('Items left after deleting {}: {}'.format(str(name),str(resp.text)), True, True)
    return  status_code,content

def reset_data_base_to_default_items(address, port):
    logger.info('Resetting data base to default items... ', True, True)
    url = 'http://{}:{}/items/'.format(address, port)
    resp = requests.get(url)
    _assert_equal(resp.status_code, 200)
    data=json.loads(resp.text)
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
    resp = requests.get(url)
    logger.info('Items after resetting : {}'.format(str(resp.text)), True, True)

def verify_response_code(actual,expected):
    actual=int(actual)
    expected=int(expected)
    _assert_equal(actual,expected)

def verify_response_content(actual,expected):
    actual=eval(actual)
    expected=eval(expected)
    _assert_equal(actual,expected)