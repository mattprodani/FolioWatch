from apis.schwab.schwab import Schwab
from apis.seeking_alpha import SeekingAlpha
from parsers.table_parser import TableParser

import json

DIR = "compiled_tables"

def load_schwab_holdings(**kwargs):
    """
        Logs in to Schwab and saves holdings,
        and watchlist analyst ratings to csv files.
        Arguments:
            **kwargs: config and secret dict
        Returns: None
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
    df = TableParser(html).parse_analyst_ratings()
    df.to_csv(f'{DIR}/analyst_ratings.csv')
    api.close_session()
    print("Successfully loaded Schwab holdings")

def load_sa_data(**kwargs):
    """
        Loads Stock Rankings from SA and saves them as CSV files
        Args: **kwargs: config and secret dict
        Returns: None
    """
    sa = SeekingAlpha(**kwargs)
    sa.login(kwargs.get("SA_user"), kwargs.get("SA_password"))

    top_html = sa.get_top_stocks()
    TableParser(top_html).parse_sa_table().to_csv(f'{DIR}/top_stocks.csv')
    
    folio_html = sa.get_portfolio()
    TableParser(folio_html).parse_sa_table().to_csv(f'{DIR}/local.sa_folio.csv')

    sa.close_session()



