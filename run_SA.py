from APIs import SeekingAlpha
import pandas as pd
import json

config = json.load(open('config.json'))
secret = json.load(open('secret.json'))
sa = SeekingAlpha(**json.loads(open('config.json').read()))
sa.login(secret["SA_user"], secret["SA_password"])
html = sa.get_top_stocks()
print(html)
with open('top_stocks.html', 'w') as f:
    f.write(html)
df = pd.read_html(html)[0]
print(df)