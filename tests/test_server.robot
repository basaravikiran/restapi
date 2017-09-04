*** Settings ***
Library     ../lib/library_rest_helper.py
Test Setup      Verify Server Is Running
                ...    ${SERVER ADDRESS}
                ...    ${SERVER PORT}
Test Teardown   Reset Default Items
                ...    ${SERVER ADDRESS}
                ...    ${SERVER PORT}

*** Variables ***
${SERVER ADDRESS}     127.0.0.1
${SERVER PORT}        5000

*** Test Cases ***
Test Create Item
    Verify Server Is Running
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    Create Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    {'name': 'ravi', 'serial': '1001'}
    Verify Item Name In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ravi

Test Create Duplicate Item
    Verify Server Is Running
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
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

*** Keywords ***
