import json


dict =  r"""
{
    "schwab": {
        "homepage": "https://www.schwab.com/",
        "account_summary": "https://client.schwab.com/clientapps/accounts/summary/",
        "positions_data": "https://client.schwab.com/api/PositionV2/PositionsDataV2",
        "order_verification": "https://client.schwab.com/api/ts/stamp/verifyOrder",
        "order_confirmation": "https://client.schwab.com/api/ts/stamp/confirmorder",
        "watchlist_data": "https://client.schwab.com/trade/watchlist/watchlist.aspx?view=analyst_ratings"
    },
    "sa": {
        "login": "https://seekingalpha.com/account/login",
        "portfolio": "https://seekingalpha.com/account/portfolio/"
    }
}
"""

class URLs():
    def __init__(self, platform: str):
        self.__dict__ = json.loads(dict)[platform]
