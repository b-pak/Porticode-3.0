from datetime import date

import moneymovement
from models import TransferType, TransferRequestStatus, TransferRequest

base_url = 'https://api-sandbox.capitalone.com'
        # need OAuth2

client_id = '83c59ee7d6a4479c8e142422cbe9022a'
client_secret = '6d5c0077c6d4e214c6850d5f1611689e'

moneymovement.setup_oauth(client_id, client_secret, base_url)

accounts = moneymovement.get_eligible_accounts()

user_account = accounts['accounts'][1]
charity_account_1 = accounts['accounts'][2]
charity_account_2 = accounts['accounts'][3]

actors = [user_account, charity_account_1, charity_account_2]

'''
for actor in actors:
    print(actor['accountNickname'])
'''


def donate(origin, destination, amount, name):

    today = str(date.today())

    transfer_request = TransferRequest()

    transfer_request.originMoneyMovementAccountReferenceId = origin["moneyMovementAccountReferenceId"]
    transfer_request.destinationMoneyMovementAccountReferenceId = destination["moneyMovementAccountReferenceId"]
    transfer_request.transferAmount = amount  # Upto 2 decimal places
    transfer_request.currencyCode = "USD"  # optional Default: USD
    transfer_request.transferDate = today
    transfer_request.memo = "Donation"  # optional
    transfer_request.transferType = TransferType.ACH.value
    transfer_request.frequency = "OneTime"  # optional Default: OneTime

    transfer_response = moneymovement.initiate_transfer(transfer_request)

    transfer_id = transfer_response['transferRequestId']

    transfer_request_receipt = moneymovement.get_transfer_request(transfer_id)

    #print(transfer_request_receipt)

    '''
    filters = {
        "fromDate": "2018-11-16",
        "toDate": "2018-11-18",
        "transferType": None,
        "transferRequestStatus": None
    }

    transfer_requests = moneymovement.get_transfer_requests(user_account["moneyMovementAccountReferenceId"],
                                                            filters)

    transfers = transfer_requests['transferRequests']

    for transfer in transfers:
        print(transfer['transferRequestId'] + " " + transfer['memo'])
    '''

    print("You Donated {} {} to {}!".format(amount, "USD", name))

    man.add_experience()

if __name__ == '__main__':
    donate(user_account, charity_account_1, 1, "Unicef")








