 #This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def market_cap_api():
    '''
    To access the api from market cap
    '''
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'100',
    'convert':'USD',
    'cryptocurrency_type':'coins'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'd973daba-2bf3-4dfc-8868-0a4a42b43d82',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        return json.loads(response.text)
    
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def get_price(data,crypto):
    symbol = crypto.upper()
    for query in data['data']:
        if query['symbol']==symbol:
            return query['quote']['USD']['market_cap']

crypto = 'eth'

data = market_cap_api()
price = get_price(data,crypto)
print(f'The price of {crypto} is {price}.')