from bs4 import BeautifulSoup
import pandas as pd

def parse_analyst_ratings(html: str) -> pd.DataFrame:
    parser = BeautifulSoup(html, 'html.parser')

    table = parser.find("table")
    for row in table.tbody.find_all("tr"):
        a = [(cell, cell.find("a")) for cell in row.find_all("td") if cell.find("a")]
        for cell, a in a:
            if a.get("title") is not None:
                if 'Rating = ' in a.get("title"):
                    cell.string = a.get("title").split('Rating = ')[1]

    df = pd.read_html(str(table))[0]
    df["ticker"] = df["Name"].apply(lambda x: x.split(" ")[0])
    df["Name"] = df.Name.apply(lambda x: " ".join(x.split(' ')[1:]))
    df = df.drop(columns = ["Links"])
    return df



def parse_sa_table(html: str) -> pd.DataFrame:
    parser = BeautifulSoup(html, 'html.parser')
    for s in parser.select('span[data-test-id="top-rated-ticker-company"]'):
        s.clear()
    for s in parser.select('span[data-test-id="portfolio-ticker-company"]'):
        s.clear()
    df = pd.read_html(str(parser), index_col= 0)[0]
    return df.dropna(axis=1, how='all')