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

import moneymovement, unittest
from models import TransferType, TransferRequestStatus, TransferRequest


class MoneyMovementTest(unittest.TestCase):
    def test_moneymovement(self):

        base_url = 'https://api-sandbox.capitalone.com'
        # need OAuth2
        client_id = '83c59ee7d6a4479c8e142422cbe9022a'
        client_secret = '6d5c0077c6d4e214c6850d5f1611689e'

        moneymovement.setup_oauth(client_id, client_secret, base_url)

        accounts = moneymovement.get_eligible_accounts()
        # self.assertEqual(4, len(accounts["accounts"]))

        capitalone_savings = accounts["accounts"][0]
        capitalone_checking = accounts["accounts"][1]
        external_checking = accounts["accounts"][2]
        external_checking_2 = accounts["accounts"][3]

        print(accounts)

        print(capitalone_savings["availableBalance"])
        print()
        #print(capitalone_checking)
        print()
        # print(external_checking)
        print(external_checking_2)
        
        # POST /money-movement/transfer-requests ACH
        transfer_request = TransferRequest()
        
        transfer_request.originMoneyMovementAccountReferenceId = external_checking["moneyMovementAccountReferenceId"]
        
        transfer_request.destinationMoneyMovementAccountReferenceId = capitalone_savings["moneyMovementAccountReferenceId"]
        
        transfer_request.transferAmount = 10.45  # Upto 2 decimal places
        transfer_request.currencyCode = "USD"  # optional Default: USD
        transfer_request.transferDate = "2018-11-17"
        transfer_request.memo = "dream car"  # optional
        transfer_request.transferType = TransferType.ACH.value
        transfer_request.frequency = "OneTime"  # optional Default: OneTime
        
        transfer_response_ach = moneymovement.initiate_transfer(transfer_request)
        print(transfer_response_ach)
        #self.assertEqual(TransferRequestStatus.SCHEDULED.value, transfer_response_ach["transferRequestStatus"])
        
        print(capitalone_savings["availableBalance"])
        print()
        
        '''
        # POST /money-movement/transfer-requests Internal
        transfer_request.originMoneyMovementAccountReferenceId = capitalone_checking["moneyMovementAccountReferenceId"]
        transfer_request.transferType = TransferType.INTERNAL.value
        
        transfer_response_internal = moneymovement.initiate_transfer(transfer_request)
        self.assertEqual(TransferRequestStatus.SCHEDULED.value, transfer_response_internal["transferRequestStatus"])
        
        
        # GET /money-movement/transfer-requests/{transferRequestId}
        transfer_request_id = transfer_response_ach["transferRequestId"]
        transfer_request_ach = moneymovement.get_transfer_request(transfer_request_id)
        self.assertEqual(transfer_request_id, transfer_request_ach["transferRequestId"])
        '''
        
        # GET /money-movement/transfer-requests
        filters = {
            "fromDate": "2018-11-16",
            "toDate": "2018-11-18",
            "transferType": None,
            "transferRequestStatus": None
        }
        
        transfer_requests = moneymovement.get_transfer_requests(capitalone_savings["moneyMovementAccountReferenceId"], filters)

        transfers = transfer_requests['transferRequests']

        for transfer in transfers:
            print(transfer['transferRequestId'] + transfer['memo'])
        
        print(transfer_requests)
        
        #self.assertEqual(transfer_requests["transferRequests"][0]["transferType"], TransferType.ACH.value);

        '''
        # PATCH /money-movement/transfer-requests/{transferRequestId}
        moneymovement.update_transfer_request(transfer_request_id, TransferRequestStatus.CANCELLED.value)
        '''


if __name__ == '__main__':
    unittest.main()
