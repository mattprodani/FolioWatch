import pandas as pd
import json
from datetime import date
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import plotly.express as px


SA_RATING = ['Price', 'Quant', 'SA Authors', 'Wall St.']
RATING_COLS = ['Symbol', 'Name', 'Price', 'Quant', 'SA Authors', 'Wall St.', 'Rating',
       'CFRA Star Ranking', 'Credit Suisse', 'Morningstar', 'Argus Rating',
       'Reuters']
STATS_COLS = ['Price', 'Change', 'Change %', 'Volume', 'Avg. Vol', 'Prev Close',
       'Open', 'Day Range', '52W Range']


def create_report():
    """
        Creates a report from the data in the portfolio.
    """
    TODAY = date.today().strftime("%Y-%m-%d")

    env = Environment(loader=FileSystemLoader('.'))


    schwab_df = pd.read_csv("compiled_tables/analyst_ratings.csv").convert_dtypes()
    sa_df = pd.read_csv("compiled_tables/local.sa_folio.csv", index_col= 0).convert_dtypes()
    schwab_holdings = json.load(open("compiled_tables/local.schwab_holdings.json"))
    global xy
    tables = []

    tables.append(create_ratings_table(sa_df, schwab_df))
    tables.append(create_stats_table(sa_df))
    pdf_plot, html_plot = plots_from_holdings(schwab_holdings)

    var_html = {
        "title": "My Daily Portfolio Report",
        "date": TODAY,
        "tables" : tables, 
        "piedata" : html_plot
    }
    var_pdf = {
        "title": "My Daily Portfolio Report",
        "date": TODAY,
        "tables" : tables, 
        "piedata" : pdf_plot
    }

    template = env.get_template("template/template.html.jinja")
    html = template.render(var_html)
    with open(f"reports/report_{TODAY}.html", "w") as f:
        f.write(html)

    html_2_pdf = env.get_template("template/pdftemplate.jinja").render(var_pdf)
    HTML(string=html_2_pdf).write_pdf(f"reports/report{TODAY}.pdf", presentational_hints=True)
    
def create_stats_table(sa):
    """
        Creates a table of stats for the portfolio holdings
    """
    sa = sa.loc[:, STATS_COLS].reset_index()
    return {"title": "Performance Update", "columns": sa.columns, "rows": sa.values}

def create_ratings_table(sa, schwab):
    """
        Creates a table of analyst ratings for the portfolio holdings
    """
    sa = sa.loc[:, SA_RATING]
    table = sa.join(schwab.set_index("ticker")).reset_index()
    table = table.loc[["CUR:" not in x for x in table.Symbol]].fillna("-").loc[:, RATING_COLS]
    table.columns = [x.replace("Ranking", "").replace("Star", "").replace("Rating", "").strip() for x in table.columns.values]
    return {"title": "Ratings Update", "columns": table.columns, "rows":table.values}

def pie_from_positions(holdings):
    """
        Processes positions from Schwab and saves to csv file.
    """
    def describe_pos(x):
        description = ""
        for key, val in x.items():
            description += f"{key}: {val}\n"
        return description

    positions = []
    for acc, hold in holdings.items():
        for pos in hold["positions"]:
            positions.append(pos)
    return [[x["symbol"], x["market_value"], describe_pos(x)] for x in positions]

def plots_from_holdings(holdings):
    def describe_pos(x):
        desc = ""
        for i, v in zip(x, x.index):
            desc += f"{v}: {i}\n"
        return desc

    positions = [p for x in holdings.values() for p in x["positions"]]
    df = pd.DataFrame(positions)
    df["More:"] = df[["description", "cost", "quantity"]].apply(describe_pos, axis=1)
    df = df.convert_dtypes()


    fig = px.pie(df, values='market_value', names='symbol', hover_data = ["More:"])
    plot_pdf = fig.to_image(format='svg')
    plot_html = df[["symbol", "market_value", "More:"]].to_numpy().tolist()
    return plot_pdf.decode("utf-8"), plot_html

if __name__ == "__main__":
    create_report()