
import requests
import pandas as pd
import asyncio
from io import StringIO

class Yahoo():
    """
        Retrieves all time historical data for a list of stocks
        Uses a threaded API for concurrent requests
    """
    def __init__(self, **kwargs):
        """
            Initializes Yahoo API
            Args: headers: dict of headers to use for requests
        """
        self.headers = kwargs.get("headers", None)
        self.session = requests.Session()
    
    def close_session(self):
        self.session.close()


    async def content_to_pandas(self, content):
        inp = StringIO(content.decode("utf-8"))
        df = pd.read_csv(inp, parse_dates=["Date"])
        return df

    async def async_retrieve_historicals(self, ticker):
        """
            Retrieves all historical price data for stock
        """
        response = self.session.get(self.download_link(ticker), headers = self.headers)
        df = await self.content_to_pandas(response.content)
        return df
    
    async def retrieve_multiples(self, tickers):
        res = await asyncio.gather(*[self.async_retrieve_historicals(ticker) for ticker in tickers])
        return res

    def load(self, tickers, threads = True):
        if isinstance(tickers, str): tickers = [tickers]
        
        if threads:
            return asyncio.run(self.retrieve_multiples(tickers))
        else:
            return [asyncio.run(self.async_retrieve_historicals(t)) for t in tickers]


    def _download_link(ticker):
        today = round(pd.Timestamp.utcnow().floor( freq = "D").timestamp())
        out = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=0&period2={today}&interval=1d&events=history&includeAdjustedClose=true"
        return out

