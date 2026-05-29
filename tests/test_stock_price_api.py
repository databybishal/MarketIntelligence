import os
import sys
import requests
import pandas as pd
import json




sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.apiSource import source
from utils import extractApis

data = source['stock_price_apis']['api']


if __name__ == '__main__':

    extract_data = extractApis(data) #because it time limit go
    print(extract_data)

    
  

    


