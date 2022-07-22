from scripts import *
import json
import getopt, sys

config = json.load(open('config.json'))
secrets = json.load(open('secret.json'))

def schwab():
    load_schwab_holdings(**secrets, **config)
def sa():
    load_sa_data(config, secrets["SA_user"], secrets["SA_password"])


def main():
    args = sys.argv[1:]
    options = "p:"
    long_options = ["platform="]
    try:
        args, vals = getopt.getopt(args, options, long_options)
        for arg, val in args:
            if arg not in ('-p', "--platform"):
                print("Invalid argument: " + arg)
                sys.exit(1)
            if val == 'schwab':
                schwab()
            elif val in ('seeking_alpha', 'sa'):
                sa()
            else:
                print("Invalid platform: " + val)
                sys.exit(1)
    except getopt.error as err:
        print (str(err))

if __name__ == "__main__":
    main()
    sys.exit(0)
