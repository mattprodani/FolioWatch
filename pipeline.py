from helpers.loaders import *
import json
from helpers.create_report import create_report
from apis.gmail import Gmail
import getopt, sys

config = json.load(open('config.json'))
secrets = json.load(open('secret.json'))


def main():
    load_schwab_holdings(**secrets, **config)
    load_sa_data(**secrets, **config)
    path = create_report()
    gmail = Gmail()

    to = config.get("email_receiver")

    pdf_path = path + ".pdf"
    
    with open(path + ".html", "rt") as f:
        body = f.read()
    gmail.send_email(to, "Your Folio Report", body, pdf_path)

if __name__ == "__main__":
    main()
    sys.exit(0)
