import os
import sys
import logging
from apiSource.data_source import source


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils import extractApis


log = logging.getLogger('ingestion')

api = source['stock_price_apis']['api']

if __name__ == '__main__':
    
    




