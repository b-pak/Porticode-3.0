#
# SPDX-Copyright: Copyright 2018 Capital One Services, LLC
# SPDX-License-Identifier: MIT
# Copyright 2018 Capital One Services, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#

import requests

OAUTH_ENDPOINT = "/oauth/oauth20/token"
MONEY_MOVEMENT = "/money-movement"
TRANSFER_REQUESTS = "/transfer-requests"
ACCOUNTS = "/accounts"


def setup_oauth(client_id, client_secret, base_url):
    global CAPITAL_ONE_SANDBOX
    CAPITAL_ONE_SANDBOX = base_url
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    oauth_headers = {
        'Accept': "application/json",
        'Content-Type': "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(CAPITAL_ONE_SANDBOX + OAUTH_ENDPOINT, data=payload, headers=oauth_headers)
        response.raise_for_status()
        json_response = response.json()

        access_token = json_response['token_type'] + ' ' + json_response['access_token']
        global api_headers
        api_headers = {
            'Accept': "application/json;v=0",
            'Authorization': access_token
        }
    except requests.exceptions.HTTPError as error:
        print(error, "\n", response.json())


def get_eligible_accounts():
    url = CAPITAL_ONE_SANDBOX + MONEY_MOVEMENT + ACCOUNTS
    try:
        response = requests.get(url, headers=api_headers)
        response.raise_for_status()
        print("Get Accounts Successful")
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(error, "\n", response.json())
 

def initiate_transfer(transfer_request):
    url = CAPITAL_ONE_SANDBOX + MONEY_MOVEMENT + TRANSFER_REQUESTS
    try:
        response = requests.post(url, json=transfer_request.__dict__, headers=api_headers)
        response.raise_for_status()
        print("Post Transfer Request Successful")
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(error, "\n", response.json())


def get_transfer_request(transfer_request_id):
    url = CAPITAL_ONE_SANDBOX + MONEY_MOVEMENT + TRANSFER_REQUESTS + "/" + transfer_request_id
    try:
        response = requests.get(url, headers=api_headers)
        response.raise_for_status()
        print("Get Transfer Request Successful")
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(error, "\n", response.json())


def get_transfer_requests(account_reference_id, filters):
    filters["moneyMovementAccountReferenceId"] = account_reference_id
    url = CAPITAL_ONE_SANDBOX + MONEY_MOVEMENT + TRANSFER_REQUESTS
    try:
        response = requests.get(url, params=filters, headers=api_headers)
        response.raise_for_status()
        print("Get Transfer Requests Successful")
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(error, "\n", response.json())


def update_transfer_request(transfer_request_id, status):
    transfer_request = {
        "transferRequestStatus": status
    }
    url = CAPITAL_ONE_SANDBOX + MONEY_MOVEMENT + TRANSFER_REQUESTS + "/" + transfer_request_id
    try:
        response = requests.patch(url, json=transfer_request, headers=api_headers)
        print("Update Transfer Request Successful")
    except requests.exceptions.HTTPError as error:
        print(error, "\n", response.json())
