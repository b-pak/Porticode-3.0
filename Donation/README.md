# Money Movement

## Setup

### Requirements

- Python 3.6.3+

- Requests ```pip3 install requests --trusted-host pypi.python.org```
 
### Running Demo

- Set ```base_url, client_id & client_secret in moneymovement_test.py```
 
- Run ```python3 -m unittest moneymovement_test.py```

## Sample Usage

```python
import moneymovement
from models import TransferType, TransferRequestStatus, TransferRequest

base_url = ... # Capital One Sandbox URL
client_id = ... # Client Id of the registered app at developer.capitalone.com
client_secret = ... # Client Secret of the registered app at developer.capitalone.com

moneymovement.setup_oauth(client_id, client_secret, base_url)

# GET /money-movement/accounts
accounts = moneymovement.get_eligible_accounts()
capitalone_savings = accounts["accounts"][0]
capitalone_checking = accounts["accounts"][1]
external_checking = accounts["accounts"][2]

# POST /money-movement/transfer-requests ACH
transfer_request = TransferRequest()
transfer_request.originMoneyMovementAccountReferenceId = external_checking["moneyMovementAccountReferenceId"]
transfer_request.destinationMoneyMovementAccountReferenceId = capitalone_savings["moneyMovementAccountReferenceId"]
transfer_request.transferAmount = 1000.45  # Upto 2 decimal places
transfer_request.currencyCode = "USD"  # optional Default: USD
transfer_request.transferDate = "2018-04-15"
transfer_request.memo = "dream car"  # optional
transfer_request.transferType = TransferType.ACH.value
transfer_request.frequency = "OneTime" # optional Default: OneTime
transfer_response_ach = moneymovement.initiate_transfer(transfer_request)

# POST /money-movement/transfer-requests Internal
transfer_request.originMoneyMovementAccountReferenceId = capitalone_checking["moneyMovementAccountReferenceId"]
transfer_request.transferType = TransferType.INTERNAL.value
transfer_response_internal = moneymovement.initiate_transfer(transfer_request)

# GET /money-movement/transfer-requests/{transferRequestId}
transfer_request_id = transfer_response_ach["transferRequestId"]
transfer_request_ach = moneymovement.get_transfer_request(transfer_request_id)

# GET /money-movement/transfer-requests
filters = {
    "fromDate": "2018-01-01",
    "toDate": "2018-04-30",
    "transferType": TransferType.ACH.value,
    "transferRequestStatus": TransferRequestStatus.SCHEDULED.value
}
transfer_requests = moneymovement.get_transfer_requests(capitalone_savings["moneyMovementAccountReferenceId"], filters)

# PATCH /money-movement/transfer-requests/{transferRequestId}
moneymovement.update_transfer_request(transfer_request_id, TransferRequestStatus.CANCELLED.value)
```

## Licence

MIT License
