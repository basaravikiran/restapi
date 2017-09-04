*** Settings ***
Library     ../lib/library_rest_helper.py
Test Setup      Verify Server Is Running
                ...    ${SERVER ADDRESS}
                ...    ${SERVER PORT}
Test Teardown   Reset Data Base To Default Items
                ...    ${SERVER ADDRESS}
                ...    ${SERVER PORT}

*** Variables ***
${SERVER ADDRESS}     127.0.0.1
${SERVER PORT}        5000

*** Test Cases ***
Test Create Item
    Create Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    {'name': 'ravi', 'serial': '1001'}
    Verify Item Name In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ravi

Test Create Duplicate Item
    Create Duplicate Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    {'name': 'kiran'}
    Delete Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    kiran
    Verify Item Name Not In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    kiran

Test Delete Non Existing Item
    Delete Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    kiran

*** Keywords ***
