import os 
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils import extractApis

simple_url = 'https://api.freeapi.app/api/v1/public/randomusers/user/random'


if __name__ == '__main__':
    dict = extractApis(simple_url)
    data = dict['data']
    print(data)
    print(type(data))
    
    


