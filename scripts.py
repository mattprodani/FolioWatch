from apis.schwab.schwab import Schwab
from apis.seeking_alpha import SeekingAlpha
from parsers.parser import *

import json

DIR = "compiled_tables"

def load_schwab_holdings(**kwargs):
    """
        Logs in to Schwab and saves holdings,
        and watchlist analyst ratings to csv files.
        Arguments:
            **kwargs: config and secret dict
    """
    api = Schwab()
    logged_in = api.login(
        username=kwargs.get("username"),
        password=kwargs.get("password"),
        totp_secret=kwargs.get("totp_secret")
    )

    assert logged_in

    print("Getting account holdings information")
    account_info = api.get_account_info()

    json.dump(account_info, open(f'{DIR}/local.schwab_holdings.json', 'w'))

    print("Getting analyst ratings")
    html = api.get_analyst_ratings()
    df = parse_analyst_ratings(html)
    df.to_csv(f'{DIR}/analyst_ratings.csv')

    print("Successfully loaded Schwab holdings")

def load_sa_data(**kwargs):
    """
        Loads Stock Rankings from SA
    """
    sa = SeekingAlpha(kwargs)
    sa.login(kwargs.get("SA_user"), kwargs.get("SA_password"))

    html = sa.get_top_stocks()
    df = parse_top_stocks(html)
    df.to_csv(f'{DIR}/top_stocks.csv')

