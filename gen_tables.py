import sys

from modules.reader import getConfig
from modules.sqlclient import SQLClient

if __name__ == '__main__':
    result, conf = getConfig()

    if not result:
        print "[Error] Failed to read config file"
        sys.exit(1)

    sqlclient = SQLClient(conf.get('user'), conf.get('password'), conf.get('host'), conf.get('dbname'))
    sqlclient.create_tables()   
    sys.exit(0)

