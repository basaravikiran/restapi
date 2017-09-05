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
  @{resp}  Create Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    {'name': 'ravi', 'serial': '1001'}
    Verify Item Name In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    ravi
    Verify Response Code
    ...     @{resp}[0]
    ...     201

Test Create Duplicate Item
    @{resp}  Create Duplicate Item
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
    Verify Response Code
    ...     @{resp}[0]
    ...     400

Delete Existing Item And Verify Response
    @{resp}  Delete Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    item_1
    verify response code
    ...     @{resp}[0]
    ...     204
    Verify Item Name Not In List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    item_1


Delete Non Existing Item And Verify Response
    @{resp}  Delete Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    item_10
    verify response code
    ...     @{resp}[0]
    ...     404
    verify response content
    ...     @{resp}[1]
    ...     {"error": "Item not found: item_10"}

Create Item Without Name Perameter And Verify Responce
    @{resp}  Create Item
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    {'firstname': 'ravi', 'lastname': 'kiran'}
    Verify Response Code
    ...     @{resp}[0]
    ...     400
    verify response content
    ...     @{resp}[1]
    ...     {'error': 'Name required!'}

Verify Response Code Non Existing Item Details Are Accessed
    @{resp}  Access Item Details
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    abcde
    Verify Response Code
    ...     @{resp}[0]
    ...     404

Verify Response Code When Existing Item Details Are Accessed
    @{resp}  Access Item Details
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    ...    item_1
    Verify Response Code
    ...     @{resp}[0]
    ...     200

Verify Response Code When Items List Is Accessed
    @{resp}  Access Items List
    ...    ${SERVER ADDRESS}
    ...    ${SERVER PORT}
    Verify Response Code
    ...     @{resp}[0]
    ...     200


*** Keywords ***

