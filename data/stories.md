<!-- Conversational: -->

## greet
* greet
  - utter_greet
  - utter_bot_function
  - action_bot_function

## builder
* builder
  - utter_builder

## thank
* thank
  - utter_thank

## react_positive
* react_positive
  - utter_react_positive

## affirm
* affirm
  - utter_affirm

## deny
* canthelp
  - utter_canthelp

## out_of_scope
* out_of_scope
  - utter_out_of_scope

## bye
* bye
  - utter_bye

<!-- Task Oriented: -->

<!-- Crypto Prices: -->

## crypto_price
* crypto_price{"crypto": "xrp"}
  - crypto_form
  - form{"name": "crypto_form"}
  - form{"name": "null"}
  - action_query_price

## crypto_historical_price + bitcoin
* crypto_historical_price{"crypto": "btc"}
  - action_query_price_date

## crypto_historical_price + eth
* crypto_historical_price{"crypto": "eth"}
  - action_query_price_date

<!-- Crypto Market Performance -->

## crypto_marketcap
* crypto_marketcap{"crypto": "btc"}
  - crypto_form
  - form{"name": "crypto_form"}
  - form{"name": "null"}
  - action_query_marketcap

## crypto_volume
* crypto_volume
  - action_query_volume

## crypto_percent_change_1h
* crypto_percent_change_1h{"crypto": "btc"}
  - action_query_percent_change_1h

## crypto_percent_change_24h
* crypto_percent_change_24h{"crypto": "bch"}
  - action_query_percent_change_24h

## highest_trading_volume
* highest_trade_volume
  - action_crypto_highest_trade_volume

## lowest_trading_volume
* lowest_trade_volume
  - action_crypto_lowest_trade_volume

## crypto_lowest_profit
* crypto_lowest_profit{"crypto":"btc"}
  - action_crypto_lowest_profit

## crypto_highest_profit
* crypto_highest_profit{"crypto":"eth"}
  - action_crypto_highest_profit
    
<!-- Crypto General Details: -->

## crypto_coin_symbol
* crypto_coin_symbol{"crypto": "btc"}
  - action_query_coin_symbol

## crypto_description
* crypto_description{"crypto": "btc"}
  - action_query_description

## crypto_feature
* crypto_feature{"crypto": "xrp"}
  - action_query_feature

## crypto_rank
* crypto_rank
  - action_query_rank

## crypto_creator
* crypto_creator{"crypto": "bch"}
  - action_query_creator

## reset_slots
* reset_slots
  - action_reset_slots

## price_trend
* price_trend{"crypto" : "eth"}
  - crypto_form
  - form{"name": "crypto_form"}
  - form{"name": "null"}
  - action_price_trend