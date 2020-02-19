# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Text, Any, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa.core.events import FollowupAction

import pandas as pd 
import datetime
import re

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from rasa_sdk.events import AllSlotsReset
import json

# Call Coin Market API
def market_cap_api():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'100',
        'convert':'USD',
        'cryptocurrency_type':'coins'
        }
    headers = {'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'd973daba-2bf3-4dfc-8868-0a4a42b43d82',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        return json.loads(response.text)    
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

# Get price of cryptos from API
def get_price(data,crypto):
    symbol = crypto.upper()
    for query in data['data']:
        if query['symbol']==symbol:
            return query['quote']['USD']['price'],query['quote']['USD']['last_updated']

# Get marketcap of cryptos from API
def get_marketcap(data,crypto):
    symbol = crypto.upper()
    for query in data['data']:
        if query['symbol'] == symbol:
            return query['quote']['USD']['market_cap'],query['quote']['USD']['last_updated']

# Get volume of cryptos from API
def get_volume(data,crypto):
    symbol = crypto.upper()
    for query in data['data']:
        if query['symbol'] == symbol:
            return query['quote']['USD']['volume_24h'],query['quote']['USD']['last_updated']

# NEW - Get all crypto's trading volume in a dictionary from API
def cryptotradingvolume(data):
    symbol = ['BTC','BCH','XRP','ETH']
    return {symbols:float(query['quote']['USD']['volume_24h']) for symbols in symbol for query in data['data'] if symbols == query['symbol']}

# Get percent change 1h of cryptos from API
def get_percentchange1h(data,crypto):
    symbol = crypto.upper()
    for query in data['data']:
        if query['symbol'] == symbol:
            return query['quote']['USD']['percent_change_1h'],query['quote']['USD']['last_updated']

# Get percent change 24h of cryptos from API
def get_percentchange24h(data,crypto):
    symbol = crypto.upper()
    for query in data['data']:
        if query['symbol'] == symbol:
            return query['quote']['USD']['percent_change_24h'],query['quote']['USD']['last_updated']

# Load crypto csvs into df
def csvtopandas(crypto):
    df = pd.read_csv('cryptodata/'+ crypto +'usd.csv',usecols=[1,2,3,4,5],parse_dates=['Date'])
    df = df.set_index('Date').sort_index(ascending=True)
    df.dropna(inplace=True)
    return df

# Query historical crypto price on date
def querypricedate(crypto, date):
    df = csvtopandas(crypto)
    # If date has the format of YYYY-MM-DD
    if re.match(r'\d{4}-\d{2}-\d{2}',date) != None:
        if df[df.index == date].empty == False:
            return df[df.index == date]['Close'][0]
        else:
            return None
    # If date has the string of Today/today/now/current
    elif date == "Today" or date == "today" or date == "now" or date == "current":
        date = datetime.datetime.now().date()
        if df[df.index == date].empty == False:
            return df[df.index == date]['Close'][0]
        else:
            return None
    # If date has the string of Yesterday/yesterday/ytd/
    elif date == "Yesterday" or date == "yesterday" or date == "ytd":
        date = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d')
        if df[df.index == date].empty == False:
            return df[df.index == date]['Close'][0]
        else:
            return None

# Query details of cryptos (Symbol, Description, Features, Ranks, Creators)
def querycoindetails(crypto):
    df = pd.read_csv('cryptodata/coindetails.csv',sep=',',index_col=0)
    coinsymbol = [*df[df.index == crypto].index.values][0]
    description = [*df[df.index == crypto].Description.values][0]
    features = [*df[df.index == crypto].Features.values][0]
    rank = [*df[df.index == crypto]['Rank '].values][0]
    creator = [*df[df.index == crypto].Creator.values][0]
    details = {'Coinsymbol':coinsymbol,'Description':description,'Features':features,'Rank':rank,'Creator':creator}
    return details

# NEW - Compute a daily return column for a specified crypto and Query the date and value of highest, and lowest return
def dailyreturn(df):
    df['Daily Return'] = ((df.Close/df.Close.shift(1))-1)*100
    dfhigh = df[df['Daily Return'] == df['Daily Return'].max()]
    dflow = df[df['Daily Return'] == df['Daily Return'].min()]
    return {'Highest Return':{'Date':str(*dfhigh[dfhigh['Daily Return'] == dfhigh['Daily Return'].max()].index.values),
                              'Value': [*dfhigh['Daily Return'].values][0]},
            'Lowest Return':{'Date':str(*dflow[dflow['Daily Return'] == dflow['Daily Return'].min()].index.values),
                              'Value': [*dflow['Daily Return'].values][0]}               
            }

class ActionQueryPrice(Action):

    def name(self) -> Text:
         return "action_query_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
         # Get crypto from respective entity values
         crypto = tracker.get_slot('crypto')
         # Query cryto for price
         data = market_cap_api()
         price,updated = get_price(data,crypto)
         dispatcher.utter_message(f'The price of {crypto.upper()} is {round(price,2)} USD. (@ {updated[:10]} {updated[11:19]})')
         return []

class ActionQueryPriceDate(Action):

    def name(self) -> Text:
        return "action_query_price_date"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        # Get crypto, date values from respective slot and entity
        crypto = tracker.get_slot('crypto')
        date = [i['value'] for i in tracker.latest_message['entities'] if i['entity'] == 'date'][0]
        # Query crypto and date for price
        price = querypricedate(crypto,date)
        # If No price available on date -> return price not available
        if price == None:
            dispatcher.utter_message("Sorry, {}/USD rate on {} is unavailable.".format(crypto,date))
        else:
            dispatcher.utter_message("The {}/USD rate on {} is {}.".format(crypto.upper(), date, price))
        return []

class ActionQueryMarketCap(Action):

    def name(self) -> Text:
        return "action_query_marketcap"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        #crypto = tracker.latest_message['entities'][0]['value']
        crypto = tracker.get_slot('crypto')
        # Query cryto for market cap
        data = market_cap_api()
        marketcap,updated = get_marketcap(data,crypto)
        dispatcher.utter_message(f'The market cap of {crypto.upper()} is {marketcap} USD. (Last updated: {updated[:10]} {updated[11:19]})')
        return []

class ActionQueryVolume(Action):

    def name(self) -> Text:
        return "action_query_volume"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        crypto = tracker.get_slot('crypto')
        # Query cryto for market cap
        data = market_cap_api()
        volume,updated = get_volume(data,crypto)
        dispatcher.utter_message(f'The 24h volume of {crypto.upper()} is {volume} USD. (Last updated: {updated[:10]} {updated[11:19]})')
        return []

# NEW - Color Coded Percent Chage
class ActionQueryPercentChange1h(Action):

    def name(self) -> Text:
        return "action_query_percent_change_1h"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        crypto = tracker.get_slot('crypto')
        # Query cryto for market cap
        data = market_cap_api()
        percent_change_1h,updated = get_percentchange1h(data,crypto)
        # Color Coding Percentage Change
        if float(percent_change_1h) > 0:
            percent_change_1h = str(percent_change_1h)
            dispatcher.utter_message(f'The 1h percent change of {crypto.upper()} is {percent_change_1h}%. (Last updated: {updated[:10]} {updated[11:19]})')
        else:
            percent_change_1h = str(percent_change_1h)
            dispatcher.utter_message(f'The 1h percent change of {crypto.upper()} is {percent_change_1h}%. (Last updated: {updated[:10]} {updated[11:19]})')
        return []

# NEW - Color Coded Percent Chage
class ActionQueryPercentChange24h(Action):

    def name(self) -> Text:
        return "action_query_percent_change_24h"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        crypto = tracker.get_slot('crypto')
        # Query cryto for market cap
        data = market_cap_api()
        # Color Coding Percentage Change
        percent_change_24h,updated = get_percentchange24h(data,crypto)
        if float(percent_change_24h) > 0:
            percent_change_24h = Fore.GREEN + str(percent_change_24h)
            dispatcher.utter_message(f'The 24h percent change of {crypto.upper()} is {percent_change_24h}%. (Last updated: {updated[:10]} {updated[11:19]})')
        else:
            percent_change_24h = Fore.RED + str(percent_change_24h)
            dispatcher.utter_message(f'The 24h percent change of {crypto.upper()} is {percent_change_24h}%. (Last updated: {updated[:10]} {updated[11:19]})')
        return []

class ActionQueryCoinSymbol(Action):

    def name(self) -> Text:
        return "action_query_coin_symbol"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        crypto = tracker.get_slot('crypto')
        coinsymbol = querycoindetails(crypto)['Coinsymbol']
        dispatcher.utter_message(f'The cryptocurrency ticker for {crypto} is {coinsymbol}.')
        return []

class ActionQueryDescription(Action):

    def name(self) -> Text:
        return "action_query_description"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        crypto = tracker.get_slot('crypto')
        description = querycoindetails(crypto)['Description']
                    
        dispatcher.utter_message(f'{description}.')
        dispatcher.utter_message(template='utter_logo_'+crypto)
        #dispatcher.utter_custom_t({'image':logo_dict[crypto]})
        #dispatcher.utter_message(logo_dict[crypto])
        return []

class ActionQueryFeature(Action):

    def name(self) -> Text:
        return "action_query_feature"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        crypto = tracker.get_slot('crypto')
        features = querycoindetails(crypto)['Features']
        dispatcher.utter_message(f'The features for {crypto} are {features}.')
        return []

class ActionQueryRank(Action):

    def name(self) -> Text:
        return "action_query_rank"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        crypto = tracker.get_slot('crypto')
        rank = querycoindetails(crypto)['Rank']
        dispatcher.utter_message(f'The rank for {crypto} is {rank}.')
        return []

class ActionQueryCreator(Action):

    def name(self) -> Text:
        return "action_query_creator"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        crypto = tracker.get_slot('crypto')
        creator = querycoindetails(crypto)['Creator']
        dispatcher.utter_message(f'The creator for {crypto} is {creator}.')
        return []

# NEW CLASS ACTIONS 

class ActionCryptoHighestTradeVolume(Action):

    def name(self) -> Text:
        return "action_crypto_highest_trade_volume"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
            data = market_cap_api()
            tradevolume = cryptotradingvolume(data)
            highesttradevolumecrypto = max(tradevolume)
            dispatcher.utter_message(f'{highesttradevolumecrypto} has the highest trading volume with {tradevolume[highesttradevolumecrypto]}USD.')
            return []

class ActionCryptoLowestTradeVolume(Action):

    def name(self) -> Text:
        return "action_crypto_lowest_trade_volume"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
            data = market_cap_api()
            tradevolume = cryptotradingvolume(data)
            lowesttradevolumecrypto = min(tradevolume)
            dispatcher.utter_message(f'{lowesttradevolumecrypto} has the lowest trading volume with {tradevolume[lowesttradevolumecrypto]} USD.')
            return []

class ActionCryptoHighestProfit(Action):

    def name(self) -> Text:
        return "action_crypto_highest_profit"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
            crypto = tracker.get_slot('crypto')
            df = csvtopandas(crypto)
            date = dailyreturn(df)['Highest Return']['Date']
            value = dailyreturn(df)['Highest Return']['Value']
            print(value)
            print(date)
            dispatcher.utter_message(f'{crypto.upper()} had the highest return of {value}% on {date}.')
            return []

class ActionCryptoLowestProfit(Action):

    def name(self) -> Text:
        return "action_crypto_lowest_profit"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
            crypto = tracker.get_slot('crypto')
            df = csvtopandas(crypto)
            date = dailyreturn(df)['Lowest Return']['Date']
            value = dailyreturn(df)['Lowest Return']['Value']
            dispatcher.utter_message(f'{crypto.upper()} had the lowest return of {round(value,1)}% on {date}.')
            return []

class CryptoForm(FormAction):
    def name(self) -> Text:
        return "crypto_form"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["crypto"]
    # def slot_mappings(self) -> Dict[Text, Any]:
    #     return {"crypto": self.from_entity(entity="crypto", intent=["inform","price"])}
    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) :
        crypto = tracker.get_slot('crypto')
        dispatcher.utter_message("I'm on it boss!")

        return[]
        #return [FollowupAction(actions_dict.get(enquiry))]


class ActionResetSlots(Action):
    ''' To Reset all the slots during the conversation '''
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("There you go boss, ALL SLOTS RESET!")

         return [AllSlotsReset()]

class ActionBotFunction(Action):

    def name(self) -> Text:
        return "action_bot_function"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        # Fetch the data and store in the format used by buttons.
        #buttons = [{"title": "Live Quote of Bitcoin", "payload": "/crypto_price{'crypto':'btc'}"}, 
                    #{"title": "What's Ripple?", "payload": "/crypto_description{'crypto':'xrp'}"}]
        #dispatcher.utter_button_message('To begin with, here are some suggested enquiries:', buttons)
        return []


class ActionPriceTrend(Action):

    def name(self) -> Text:
        return "action_price_trend"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:
        
        crypto = tracker.get_slot('crypto')
        df = pd.read_csv('cryptodata/'+ crypto +'usd.csv',usecols=[1,2,3,4,5])
        df = df[['Date','Close']].dropna()
        df = df[::-1]

        n = df.shape[0]

        data = []
        for i in range(n):
            d = {}
            d['x'] = df.Date.values[i]
            d['y'] = df.Close.values[i]
            data.append(d)
        
        chart_data = {
            "payload":"chart",
            "data":{
                "title": "Price Trend of " + crypto,
                "labels": df.Date.values,
                "backgroundColor": ["#36a2eb"],
                "chartsData":data,
                "chartType":"line",
                "displayLegend":"false"
            }
        }
        dispatcher.utter_custom_json(chart_data)
        return []